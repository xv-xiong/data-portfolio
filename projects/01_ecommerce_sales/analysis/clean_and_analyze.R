# ---------------------------------------------------------------
# 01_ecommerce_sales —— 数据分析脚手架（R / tidyverse 版）
# 与 Python 版对应：同样的清洗逻辑，换成 tidyverse 写法。
# 本地需安装：install.packages(c("tidyverse","lubridate","RSQLite"))
# 运行：Rscript analysis/clean_and_analyze.R
# 注：本文件为模板，未在本机运行（环境无 R），请在你本地验证。
# ---------------------------------------------------------------
library(tidyverse)
library(lubridate)
library(RSQLite)

base <- here::here("projects", "01_ecommerce_sales")
raw <- read_csv(file.path(base, "raw", "orders_raw.csv"), show_col_types = FALSE)
clean_path <- file.path(base, "clean", "orders_clean.csv")
db_path <- file.path(base, "clean", "portfolio.db")

df <- raw %>%
  mutate(
    region = str_to_title(str_trim(region)),
    quantity = as.numeric(quantity),
    unit_price = as.numeric(unit_price),
    order_date = parse_date_time(order_date, c("ymd", "Y/m/d"), quiet = TRUE)
  ) %>%
  distinct() %>%
  filter(!is.na(order_id), !is.na(order_date),
         !is.na(quantity), !is.na(unit_price),
         quantity > 0,
         str_to_lower(str_trim(status)) == "paid") %>%
  mutate(amount = quantity * unit_price,
         order_month = floor_date(order_date, "month") %>% format("%Y-%m")) %>%
  arrange(order_date)

write_csv(df, clean_path)

# 分析
monthly <- df %>% group_by(order_month) %>% summarise(amount = sum(amount))
cat("峰值月:", monthly$order_month[which.max(monthly$amount)], "\n")

# 图表
png(file.path(base, "output", "sales_trend_r.png"), width = 800, height = 400)
plot(monthly$order_month, monthly$amount, type = "o", col = "#1f4e79",
     main = "月度销售额趋势 (R)", ylab = "销售额 (¥)", xlab = "")
dev.off()

# 导出 SQLite
con <- dbConnect(SQLite(), db_path)
dbWriteTable(con, "orders_clean", df, overwrite = TRUE)
dbDisconnect(con)

cat("R 版完成：clean/", basename(clean_path), " + output/sales_trend_r.png + SQLite\n")
