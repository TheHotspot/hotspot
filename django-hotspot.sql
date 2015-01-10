-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 21, 2014 at 10:51 PM
-- Server version: 5.5.34
-- PHP Version: 5.3.10-1ubuntu3.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `django-hotspot`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_emailaddress`
--

CREATE TABLE IF NOT EXISTS `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `email` varchar(75) COLLATE utf8_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_6340c63c` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `account_emailaddress`
--

INSERT INTO `account_emailaddress` (`id`, `user_id`, `email`, `verified`, `primary`) VALUES
(1, 4, 'nikisweeting@gmail.com', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_emailconfirmation`
--

CREATE TABLE IF NOT EXISTS `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_address_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `sent` datetime DEFAULT NULL,
  `key` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirmation_a659cab3` (`email_address_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `account_emailconfirmation`
--

INSERT INTO `account_emailconfirmation` (`id`, `email_address_id`, `created`, `sent`, `key`) VALUES
(1, 1, '2014-01-21 13:44:34', '2014-01-21 13:44:34', 'd0d718d7653965536bdd129b4ffeb652b0eb115004b0214697339643963f0a9a');

-- --------------------------------------------------------

--
-- Table structure for table `api_business`
--

CREATE TABLE IF NOT EXISTS `api_business` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `api_business`
--

INSERT INTO `api_business` (`id`, `name`, `logo`) VALUES
(1, 'Hollywood Professional Center', 'http://vpn.nicksweeting.com/images/up.gif');

-- --------------------------------------------------------

--
-- Table structure for table `api_business_user`
--

CREATE TABLE IF NOT EXISTS `api_business_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `business_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `business_id` (`business_id`,`user_id`),
  KEY `api_business_user_311726d6` (`business_id`),
  KEY `api_business_user_6340c63c` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `api_business_user`
--

INSERT INTO `api_business_user` (`id`, `business_id`, `user_id`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `api_checkin`
--

CREATE TABLE IF NOT EXISTS `api_checkin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `hotspot_id` int(11) NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_checkin_6340c63c` (`user_id`),
  KEY `api_checkin_264e9f0a` (`hotspot_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=8 ;

--
-- Dumping data for table `api_checkin`
--

INSERT INTO `api_checkin` (`id`, `user_id`, `hotspot_id`, `time_in`, `time_out`) VALUES
(1, 1, 1, '2014-01-19 00:56:58', '2014-01-19 06:45:34'),
(2, 1, 2, '2014-01-19 00:58:10', '2014-01-19 02:38:26'),
(3, 2, 1, '2014-01-19 01:50:33', '2014-01-19 05:23:30'),
(4, 2, 1, '2014-01-19 05:19:12', '2014-01-19 05:23:30'),
(5, 2, 2, '2014-01-19 05:19:12', '2014-01-19 05:23:30'),
(6, 2, 3, '2014-01-19 05:19:12', '2014-01-19 05:23:30'),
(7, 1, 3, '2014-01-19 06:37:59', '1969-12-31 16:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `api_hotspot`
--

CREATE TABLE IF NOT EXISTS `api_hotspot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `business_id` int(11) NOT NULL,
  `LAT` double NOT NULL,
  `LNG` double NOT NULL,
  `description` varchar(1000) COLLATE utf8_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_hotspot_311726d6` (`business_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

--
-- Dumping data for table `api_hotspot`
--

INSERT INTO `api_hotspot` (`id`, `name`, `business_id`, `LAT`, `LNG`, `description`, `logo`) VALUES
(1, 'Hackathon Center', 1, 45.8888, -122.322, 'Where work gets done.', 'http://vpn.nicksweeting.com/images/up.gif'),
(2, 'Reception', 1, 45.8888, -122.322, 'The front desk.', 'http://vpn.nicksweeting.com/images/up.gif'),
(3, 'Empty Room', 1, 45.8888, -122.322, 'A room no one likes to visit.', 'http://vpn.nicksweeting.com/images/up.gif');

-- --------------------------------------------------------

--
-- Table structure for table `api_user`
--

CREATE TABLE IF NOT EXISTS `api_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(75) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  `telephone` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;

--
-- Dumping data for table `api_user`
--

INSERT INTO `api_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `telephone`) VALUES
(1, 'pbkdf2_sha256$12000$vlc7zfK5AzpT$8C9DCmAyNEPD4ZqTOG3mVA1Ntzct4hXLxqOyNYfrUuY=', '2014-01-21 13:44:46', 1, 'nick', 'Nick', 'Sweeting', 'nikisweeting+django@gmail.com', 1, 1, '2014-01-19 00:45:05', '5037419577'),
(2, 'blake', '2014-01-19 01:50:37', 0, 'blake', 'Blake', 'Canfield', 'blakecan@gmail.com', 0, 1, '2014-01-19 01:50:37', '000000000'),
(3, 'blah', '2014-01-19 20:15:35', 0, 'blah', 'Blah', 'mcblahson', 'nikisweeting+djangoblah@gmail.com', 0, 1, '2014-01-19 20:15:36', '000000000000000'),
(4, '!3n6jGjXUerCePNbLRtTJdJHbpJXTb9ukUEpr9Y6E', '2014-01-21 13:44:34', 0, 'nikisweeting', 'Nick', 'Sweeting', 'nikisweeting@gmail.com', 0, 1, '2014-01-21 13:44:34', '');

-- --------------------------------------------------------

--
-- Table structure for table `api_user_groups`
--

CREATE TABLE IF NOT EXISTS `api_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `api_user_groups_6340c63c` (`user_id`),
  KEY `api_user_groups_5f412f9a` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `api_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `api_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `api_user_user_permissions_6340c63c` (`user_id`),
  KEY `api_user_user_permissions_83d7f98b` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=77 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add site', 4, 'add_site'),
(11, 'Can change site', 4, 'change_site'),
(12, 'Can delete site', 4, 'delete_site'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add email address', 7, 'add_emailaddress'),
(20, 'Can change email address', 7, 'change_emailaddress'),
(21, 'Can delete email address', 7, 'delete_emailaddress'),
(22, 'Can add email confirmation', 8, 'add_emailconfirmation'),
(23, 'Can change email confirmation', 8, 'change_emailconfirmation'),
(24, 'Can delete email confirmation', 8, 'delete_emailconfirmation'),
(25, 'Can add migration history', 9, 'add_migrationhistory'),
(26, 'Can change migration history', 9, 'change_migrationhistory'),
(27, 'Can delete migration history', 9, 'delete_migrationhistory'),
(28, 'Can add user', 10, 'add_user'),
(29, 'Can change user', 10, 'change_user'),
(30, 'Can delete user', 10, 'delete_user'),
(31, 'Can add business', 11, 'add_business'),
(32, 'Can change business', 11, 'change_business'),
(33, 'Can delete business', 11, 'delete_business'),
(34, 'Can add hotspot', 12, 'add_hotspot'),
(35, 'Can change hotspot', 12, 'change_hotspot'),
(36, 'Can delete hotspot', 12, 'delete_hotspot'),
(37, 'Can add check in', 13, 'add_checkin'),
(38, 'Can change check in', 13, 'change_checkin'),
(39, 'Can delete check in', 13, 'delete_checkin'),
(40, 'Can add social app', 14, 'add_socialapp'),
(41, 'Can change social app', 14, 'change_socialapp'),
(42, 'Can delete social app', 14, 'delete_socialapp'),
(43, 'Can add social account', 15, 'add_socialaccount'),
(44, 'Can change social account', 15, 'change_socialaccount'),
(45, 'Can delete social account', 15, 'delete_socialaccount'),
(46, 'Can add social token', 16, 'add_socialtoken'),
(47, 'Can change social token', 16, 'change_socialtoken'),
(48, 'Can delete social token', 16, 'delete_socialtoken'),
(49, 'Can view business', 11, 'view_business'),
(50, 'Can view check in', 13, 'view_checkin'),
(51, 'Can view content type', 5, 'view_contenttype'),
(52, 'Can view email address', 7, 'view_emailaddress'),
(53, 'Can view email confirmation', 8, 'view_emailconfirmation'),
(54, 'Can view group', 3, 'view_group'),
(55, 'Can view hotspot', 12, 'view_hotspot'),
(56, 'Can view log entry', 1, 'view_logentry'),
(57, 'Can view migration history', 9, 'view_migrationhistory'),
(58, 'Can view permission', 2, 'view_permission'),
(59, 'Can view session', 6, 'view_session'),
(60, 'Can view site', 4, 'view_site'),
(61, 'Can view social account', 15, 'view_socialaccount'),
(62, 'Can view social app', 14, 'view_socialapp'),
(63, 'Can view social token', 16, 'view_socialtoken'),
(64, 'Can view user', 10, 'view_user'),
(65, 'Can add Bookmark', 17, 'add_bookmark'),
(66, 'Can change Bookmark', 17, 'change_bookmark'),
(67, 'Can delete Bookmark', 17, 'delete_bookmark'),
(68, 'Can add User Setting', 18, 'add_usersettings'),
(69, 'Can change User Setting', 18, 'change_usersettings'),
(70, 'Can delete User Setting', 18, 'delete_usersettings'),
(71, 'Can add User Widget', 19, 'add_userwidget'),
(72, 'Can change User Widget', 19, 'change_userwidget'),
(73, 'Can delete User Widget', 19, 'delete_userwidget'),
(74, 'Can view Bookmark', 17, 'view_bookmark'),
(75, 'Can view User Setting', 18, 'view_usersettings'),
(76, 'Can view User Widget', 19, 'view_userwidget');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=19 ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `user_id`, `content_type_id`, `object_id`, `object_repr`, `action_flag`, `change_message`) VALUES
(1, '2014-01-19 00:48:30', 1, 10, '1', 'nick', 2, 'Changed first_name, last_name and telephone.'),
(2, '2014-01-19 00:56:20', 1, 11, '1', 'Hollywood Professional Center', 1, ''),
(3, '2014-01-19 00:56:48', 1, 12, '1', 'Hackathon Center', 1, ''),
(4, '2014-01-19 00:57:08', 1, 13, '1', 'Nick Sweeting @ Hackathon Center', 1, ''),
(5, '2014-01-19 00:58:36', 1, 12, '2', 'Reception', 1, ''),
(6, '2014-01-19 00:58:39', 1, 13, '2', 'Nick Sweeting @ Reception', 1, ''),
(7, '2014-01-19 01:51:07', 1, 10, '2', 'blake', 1, ''),
(8, '2014-01-19 01:51:12', 1, 13, '3', 'Blake Canfield @ Hackathon Center', 1, ''),
(9, '2014-01-19 02:02:57', 1, 12, '3', 'Empty Room', 1, ''),
(10, '2014-01-19 06:38:13', 1, 13, '7', 'Nick Sweeting @ Empty Room', 1, ''),
(11, '2014-01-19 06:45:37', 1, 13, '1', 'Nick Sweeting @ Hackathon Center', 2, 'Changed time_out.'),
(12, '2014-01-19 20:16:30', 1, 10, '3', 'blah', 1, ''),
(13, '2014-01-21 13:04:58', 1, 4, '1', 'hotspot.nicksweeting.com', 2, 'Changed domain and name.'),
(14, '2014-01-21 13:30:06', 1, 4, '2', 'hotspot.nicksweeting.com', 1, ''),
(15, '2014-01-21 13:36:13', 1, 4, '3', 'hotspot.nicksweeting.com', 1, ''),
(16, '2014-01-21 13:36:34', 1, 14, '1', 'Hotspot', 1, ''),
(17, '2014-01-21 13:43:18', 1, 14, '2', 'Hotspot', 1, ''),
(18, '2014-01-21 13:43:54', 1, 4, '4', 'localhost', 1, '');

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=20 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'log entry', 'admin', 'logentry'),
(2, 'permission', 'auth', 'permission'),
(3, 'group', 'auth', 'group'),
(4, 'site', 'sites', 'site'),
(5, 'content type', 'contenttypes', 'contenttype'),
(6, 'session', 'sessions', 'session'),
(7, 'email address', 'account', 'emailaddress'),
(8, 'email confirmation', 'account', 'emailconfirmation'),
(9, 'migration history', 'south', 'migrationhistory'),
(10, 'user', 'api', 'user'),
(11, 'business', 'api', 'business'),
(12, 'hotspot', 'api', 'hotspot'),
(13, 'check in', 'api', 'checkin'),
(14, 'social app', 'socialaccount', 'socialapp'),
(15, 'social account', 'socialaccount', 'socialaccount'),
(16, 'social token', 'socialaccount', 'socialtoken'),
(17, 'Bookmark', 'xadmin', 'bookmark'),
(18, 'User Setting', 'xadmin', 'usersettings'),
(19, 'User Widget', 'xadmin', 'userwidget');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1w34nimx8ouv9cite1qh2bwq2ystzmes', 'YTM3MWNjMTg3NTRmNzc2ZmI0ZWNmYmUwNTExOGU0MDMxNGQ2OWFlYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=', '2014-02-02 00:45:22'),
('49jp2evq6wzm4c7s18ylxnopevu090ly', 'NTllMjcwYjk1YTIyMzBjNzY1MmFjNzkyMDZiYzgzMWMzNDFmNzllYTp7fQ==', '2014-02-04 13:36:42'),
('7v6gx4ipfwxzlq6omqts1m5we25y7ec2', 'MDJjMDA1NWNlMjA3NDQwZDU4YzY3Yzc3ODZlMTJiYWVmZjdlNWJjODp7IkxJU1RfUVVFUlkiOltbImFwaSIsInVzZXIiXSwiX3FfPW5pY2siXSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoxfQ==', '2014-02-02 06:28:15'),
('cxed9d2lr1gly74kpul38r7azb8bqe3g', 'YWJlY2E0NjFhODQ1ZGU1ZGY2NWEzYzFmY2IxNzc2ZWQ2YjgxNGZmNjp7IkxJU1RfUVVFUlkiOltbImFwaSIsInVzZXIiXSwiIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=', '2014-02-04 13:49:48'),
('pw7suy6yvs36blrdjcoorpbypjblx7os', 'YWJlY2E0NjFhODQ1ZGU1ZGY2NWEzYzFmY2IxNzc2ZWQ2YjgxNGZmNjp7IkxJU1RfUVVFUlkiOltbImFwaSIsInVzZXIiXSwiIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=', '2014-02-02 06:02:29'),
('u7lg2quap49hio17gamyns9pnkn74a2q', 'YTM3MWNjMTg3NTRmNzc2ZmI0ZWNmYmUwNTExOGU0MDMxNGQ2OWFlYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=', '2014-02-02 12:01:07'),
('yeacvwtvo5luzu8gui87brmfbdcl98iu', 'ZWJkMTYwMTU4NjViM2RkMjZhMDM3NmM1ZDc3YTViM2M0MzMxZWI1ZDp7IkxJU1RfUVVFUlkiOltbImFwaSIsInVzZXIiXSwiIl0sIl9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2014-02-02 20:13:35');

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'hotspot.nicksweeting.com', 'hotspot.nicksweeting.com'),
(4, 'localhost', 'localhost (debug)');

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialaccount`
--

CREATE TABLE IF NOT EXISTS `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `provider` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `uid` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  `extra_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_4f431f56_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_6340c63c` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `socialaccount_socialaccount`
--

INSERT INTO `socialaccount_socialaccount` (`id`, `user_id`, `provider`, `uid`, `last_login`, `date_joined`, `extra_data`) VALUES
(1, 4, 'facebook', '1256316575', '2014-01-21 13:44:34', '2014-01-21 13:44:34', '{"username": "nikisweeting", "bio": "Although Ford had taken great care to blend into Earth society, he had \\"skimped a bit on his preparatory research,\\" and thought that the name \\"Ford Prefect\\" would be \\"nicely inconspicuous.\\" Adams later clarified in an interview that Ford \\"had simply mistaken the dominant life form.\\" The Ford Prefect was, in fact, a British car manufactured from 1938 to 1961. This was expanded on somewhat in the film version, where Ford is almost run over while attempting to greet a blue Ford Prefect.", "first_name": "Nick", "last_name": "Sweeting", "verified": true, "name": "Nick Sweeting", "locale": "en_US", "hometown": {"id": "108424279189115", "name": "New York, New York"}, "work": [{"position": {"id": "137221592980321", "name": "Developer"}, "start_date": "2013-07-03", "location": {"id": "112548152092705", "name": "Portland, Oregon"}, "employer": {"id": "527957620626396", "name": "The Hotspot"}}, {"position": {"id": "108462862541974", "name": "Mechanic"}, "start_date": "2013-05-20", "location": {"id": "106324046073002", "name": "Shanghai, China"}, "end_date": "2013-07-02", "employer": {"id": "48354778001", "name": "Giant Bicycles"}}, {"description": "Sysadmin and Junior Web Dev. ", "end_date": "2013-05-10", "employer": {"id": "150400631765101", "name": "Delivery Hero China"}, "location": {"id": "106324046073002", "name": "Shanghai, China"}, "position": {"id": "137221592980321", "name": "Developer"}, "start_date": "2013-03-04"}, {"description": "\\u719f\\u6089 Windows/Mac/ Linux \\u64cd\\u4f5c\\u7cfb\\u7edf\\u53ca\\u4f7f\\u7528\\u3002\\u6309\\u6280\\u672f\\u90e8\\u4e3b\\u7ba1\\u7684\\u8981\\u6c42,\\u5b8c\\u6210\\u5bf9\\u5ba2\\u6237\\u6216\\u516c\\u53f8\\u5185\\u90e8\\u7684 IT \\u670d\\u52a1\\u4efb\\u52a1\\u3002", "end_date": "2013-07-01", "employer": {"id": "580814831986169", "name": "D&bond"}, "location": {"id": "106324046073002", "name": "Shanghai, China"}, "position": {"id": "143159379045569", "name": "Server Administrator"}, "start_date": "2013-01-07"}, {"position": {"id": "138934589460163", "name": "Sales/Mechanics"}, "start_date": "2012-09-01", "location": {"id": "106324046073002", "name": "Shanghai, China"}, "end_date": "2012-10-31", "employer": {"id": "430142320345623", "name": "Specialized"}}, {"start_date": "2012-01-01", "end_date": "0000-00", "employer": {"id": "272469712853163", "name": "make512"}}, {"description": "Sales/Retail and some occasional mechanics.", "end_date": "2012-07-01", "employer": {"id": "385060420261", "name": "MODSquad Cycles"}, "location": {"id": "108424279189115", "name": "New York, New York"}, "position": {"id": "107473202615877", "name": "Sales"}, "start_date": "2012-01-01"}], "email": "nikisweeting@gmail.com", "updated_time": "2014-01-18T22:30:10+0000", "link": "https://www.facebook.com/nikisweeting", "location": {"id": "112548152092705", "name": "Portland, Oregon"}, "gender": "male", "timezone": -8, "education": [{"school": {"id": "102092629832041", "name": "Sunset High School"}, "classes": [{"with": [{"id": "1322234254", "name": "Blake Canfield"}], "id": "195573007135761", "name": "2014"}], "type": "High School", "year": {"id": "143641425651920", "name": "2014"}}, {"school": {"id": "114977898517343", "name": "Concordia International School"}, "type": "High School", "year": {"id": "293650690709608", "name": "2012"}}, {"school": {"id": "110191742343648", "name": "SCIS Hongqiao"}, "type": "High School", "year": {"id": "142963519060927", "name": "2010"}}, {"school": {"id": "109550932404321", "name": "Fudan International School"}, "type": "High School", "year": {"id": "144044875610606", "name": "2011"}}, {"school": {"id": "350739398394661", "name": "Homeschool"}, "type": "High School", "year": {"id": "144044875610606", "name": "2011"}}], "id": "1256316575"}');

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp`
--

CREATE TABLE IF NOT EXISTS `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `client_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `key` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `secret` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Dumping data for table `socialaccount_socialapp`
--

INSERT INTO `socialaccount_socialapp` (`id`, `provider`, `name`, `client_id`, `key`, `secret`) VALUES
(2, 'facebook', 'Hotspot', '224009197757661', '', 'd7cc8a8a8b902d460a58cef66740b0fd');

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp_sites`
--

CREATE TABLE IF NOT EXISTS `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_3e6a002b_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_f2973cd1` (`socialapp_id`),
  KEY `socialaccount_socialapp_sites_99732b5c` (`site_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

INSERT INTO `socialaccount_socialapp_sites` (`id`, `socialapp_id`, `site_id`) VALUES
(2, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialtoken`
--

CREATE TABLE IF NOT EXISTS `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `token` longtext COLLATE utf8_unicode_ci NOT NULL,
  `token_secret` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `expires_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_73d1e698_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_socialtoken_60fc113e` (`app_id`),
  KEY `socialaccount_socialtoken_93025c2f` (`account_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `socialaccount_socialtoken`
--

INSERT INTO `socialaccount_socialtoken` (`id`, `app_id`, `account_id`, `token`, `token_secret`, `expires_at`) VALUES
(1, 2, 1, 'CAADLvDSopN0BAKnVX5KSE7VLRoJmDMkZAegX42yLimUw3wfVXsTbcsTY8WafWS3CAHLQHjb1jHzgql5kZBlB4IckXNXsehZCKb9tqN1JTaTuL9qu9fHFqkpk7ABVfHsZADpQtRfZAvKV6zpH85omwweFEsTr4hnk5IX2iSehP38LcP7pBsZC6wMa3ytg7T3VZC5EYyIGBZCvkwZDZD', '', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `south_migrationhistory`
--

CREATE TABLE IF NOT EXISTS `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `migration` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=21 ;

--
-- Dumping data for table `south_migrationhistory`
--

INSERT INTO `south_migrationhistory` (`id`, `app_name`, `migration`, `applied`) VALUES
(14, 'django_extensions', '0001_empty', '2014-01-19 11:57:56'),
(15, 'api', '0001_do', '2014-01-19 12:00:35'),
(16, 'django_extensions', '0002_initial', '2014-01-21 13:08:13'),
(17, 'socialaccount', '0001_new', '2014-01-21 13:12:25'),
(18, 'facebook', '0001_new', '2014-01-21 13:12:25'),
(19, 'socialaccount', '0002_initial', '2014-01-21 13:34:38'),
(20, 'facebook', '0002_initial', '2014-01-21 13:35:09');

-- --------------------------------------------------------

--
-- Table structure for table `xadmin_bookmark`
--

CREATE TABLE IF NOT EXISTS `xadmin_bookmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `url_name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `query` varchar(1000) COLLATE utf8_unicode_ci NOT NULL,
  `is_share` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_bookmark_6340c63c` (`user_id`),
  KEY `xadmin_bookmark_37ef4eb4` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `xadmin_usersettings`
--

CREATE TABLE IF NOT EXISTS `xadmin_usersettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `key` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `value` longtext COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_usersettings_6340c63c` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `xadmin_usersettings`
--

INSERT INTO `xadmin_usersettings` (`id`, `user_id`, `key`, `value`) VALUES
(1, 1, 'dashboard:home:pos', '');

-- --------------------------------------------------------

--
-- Table structure for table `xadmin_userwidget`
--

CREATE TABLE IF NOT EXISTS `xadmin_userwidget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `page_id` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `widget_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `value` longtext COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_userwidget_6340c63c` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  ADD CONSTRAINT `user_id_refs_id_44632e47` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  ADD CONSTRAINT `email_address_id_refs_id_6ea1eea3` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`);

--
-- Constraints for table `api_business_user`
--
ALTER TABLE `api_business_user`
  ADD CONSTRAINT `business_id_refs_id_f7b78038` FOREIGN KEY (`business_id`) REFERENCES `api_business` (`id`),
  ADD CONSTRAINT `user_id_refs_id_f5578bfd` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `api_checkin`
--
ALTER TABLE `api_checkin`
  ADD CONSTRAINT `hotspot_id_refs_id_8dbaf894` FOREIGN KEY (`hotspot_id`) REFERENCES `api_hotspot` (`id`),
  ADD CONSTRAINT `user_id_refs_id_dc076598` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `api_hotspot`
--
ALTER TABLE `api_hotspot`
  ADD CONSTRAINT `business_id_refs_id_3a16751c` FOREIGN KEY (`business_id`) REFERENCES `api_business` (`id`);

--
-- Constraints for table `api_user_groups`
--
ALTER TABLE `api_user_groups`
  ADD CONSTRAINT `group_id_refs_id_18d59539` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `user_id_refs_id_d30a7285` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `api_user_user_permissions`
--
ALTER TABLE `api_user_user_permissions`
  ADD CONSTRAINT `permission_id_refs_id_27455f0c` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `user_id_refs_id_598ad5a8` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `user_id_refs_id_9edf0019` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  ADD CONSTRAINT `user_id_refs_id_46fb7633` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `socialaccount_socialapp_sites`
--
ALTER TABLE `socialaccount_socialapp_sites`
  ADD CONSTRAINT `site_id_refs_id_05d6147e` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`),
  ADD CONSTRAINT `socialapp_id_refs_id_e7a43014` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`);

--
-- Constraints for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  ADD CONSTRAINT `account_id_refs_id_1337a128` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  ADD CONSTRAINT `app_id_refs_id_edac8a54` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`);

--
-- Constraints for table `xadmin_bookmark`
--
ALTER TABLE `xadmin_bookmark`
  ADD CONSTRAINT `content_type_id_refs_id_af66fd92` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `user_id_refs_id_67958439` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `xadmin_usersettings`
--
ALTER TABLE `xadmin_usersettings`
  ADD CONSTRAINT `user_id_refs_id_a4558ddd` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

--
-- Constraints for table `xadmin_userwidget`
--
ALTER TABLE `xadmin_userwidget`
  ADD CONSTRAINT `user_id_refs_id_a8663dc3` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
