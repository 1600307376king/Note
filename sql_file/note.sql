/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : note

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2019-11-09 17:43:17
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for notes
-- ----------------------------
DROP TABLE IF EXISTS `notes`;
CREATE TABLE `notes` (
  `n_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `note_title` varchar(255) DEFAULT NULL,
  `note_labels` varchar(255) DEFAULT NULL,
  `note_content` text DEFAULT NULL,
  `note_instructions` text DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  PRIMARY KEY (`n_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of notes
-- ----------------------------
INSERT INTO `notes` VALUES ('11', 'd7675e1e-02c0-11ea-9a1a-001a7dda7113', 'Python基础第一周', 'Python |', '\n####2.1.3 Unix & Linux 平台安装 Python:(源码式安装\n* 以下为在Unix & Linux 平台上安装 Python 的简单步骤：\n* 打开WEB浏览器访问http://www.python.org/download/\n* 选择适用于Unix/Linux的源码压缩包。\n\n##### 2.1.4 通过ubuntu官方的apt工具包安装\n    $ sudo apt-get install python\n    $ sudo apt-get install python2.7\n    $ sudo apt-get install python3.7\n    dddd\n\n\n\n\n\n\n', '                                                                                                                                                Python 是一个高层次的结合了解释性、编译性、互动性和面向对象的脚本语言。\n\n简单来说，Python是一门编程语言，帮助我们更好的与计算机沟通，功能全面、易学易用、可拓展语言，所以说，人生苦短，我学Python。\n                    \n                    \n                    \n                    \n                    \n                    \n                    ', '2019-11-09 15:16:25');
