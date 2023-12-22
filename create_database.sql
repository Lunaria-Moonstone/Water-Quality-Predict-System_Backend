-- create database
CREATE DATABASE IF NOT EXISTS water_quality_pred_sys;
USE water_quality_pred_sys;
-- create table
CREATE TABLE IF NOT EXISTS `user` (
  `id` CHAR(36) PRIMARY KEY COMMENT "账户唯一标识",
  `name` VARCHAR(16) NOT NULL UNIQUE COMMENT "账户登录名",
  `password` VARCHAR(128) NOT NULL COMMENT "账户密码",
  `active` BOOLEAN DEFAULT 1 COMMENT "账户是否可用",
  `root` BOOLEAN DEFAULT 0 COMMENT "是否根管理员",
  `created` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "账户创建时间",
  `updated` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "账户更新时间"
);
CREATE TABLE IF NOT EXISTS `sample` (
  `id` CHAR(32) PRIMARY KEY COMMENT "样本唯一标识",
  `created` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "样本创建时间",
  `updated` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "样本更新时间"
);
CREATE TABLE IF NOT EXISTS `samples_preload` (
  `id` CHAR(32) PRIMARY KEY COMMENT "预录入样本集唯一标识",
  `name` VARCHAR(64) NOT NULL COMMENT "预录入样本集文件名称",
  `fetched` DATETIME NOT NULL COMMENT "预录入样本集采集时间",
  `created` DATETIME NOT NULL COMMENT "预录入样本集记录写入时间"
);
CREATE TABLE IF NOT EXISTS `model` (
  `id` CHAR(32) PRIMARY KEY COMMENT "模型唯一标识",
  `name` VARCHAR(64) NOT NULL COMMENT "模型备注名称",
  `parent_id` CHAR(32) COMMENT "模型父节点"
);
CREATE TABLE IF NOT EXISTS `logging` (
  `id` CHAR(32) PRIMARY KEY COMMENT "日志唯一标识",
  `level` TINYINT NOT NULL COMMENT "0-info 1-debug 2-warning 3-error",
  `filename` VARCHAR(64) NOT NULL COMMENT "生成日志文件",
  `funcname` VARCHAR(64) NOT NULL COMMENT "生成日志方法",
  `datetime` DATETIME NOT NULL COMMENT "日志记录时间",
  `descript` VARCHAR(256) COMMENT "日志描述"
);