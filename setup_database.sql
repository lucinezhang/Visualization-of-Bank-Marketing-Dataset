CREATE DATABASE  IF NOT EXISTS `bank` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `bank`;

-----------------------------------------------------------------------
---- Create Tables
-----------------------------------------------------------------------

-----------------------------------------------------------------------
---- Create Tables Comments
-----------------------------------------------------------------------
DROP TABLE IF EXISTS `original`;
CREATE TABLE original
(
  age  int,
  job  varchar(20),
  marital  varchar(20),
  education  varchar(20),
  def  varchar(20),
  balance int,
  housing varchar(20),
  loan varchar(20),
  contact varchar(20),
  day int,
  month varchar(5),
  duration int,
  campaign int,
  pdays int,
  previous int,
  poutcome varchar(20),
  y varchar(5)
);

LOAD DATA LOCAL INFILE '~/Desktop/BankMarketingDataSet-master/data/bank-full.csv' 
INTO TABLE original 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 

