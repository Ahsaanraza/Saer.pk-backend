-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 25, 2025 at 03:29 PM
-- Server version: 11.4.8-MariaDB-cll-lve-log
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `saerkaro_testapi`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(22, 'one'),
(21, 'CC'),
(20, 'two'),
(19, 'group 1'),
(24, 'SJXN');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(45, 'Mubeen Abbas', 2, 'Booking'),
(55, 'Can add log entry', 1, 'add_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(61, 'Can delete user files', 12, 'delete_userfiles'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(58, 'Can view log entry', 1, 'view_logentry'),
(59, 'Can add group', 3, 'add_group'),
(60, 'Can change user files', 12, 'change_userfiles'),
(29, 'Can add permission extension', 8, 'add_permissionextension'),
(30, 'Can change permission extension', 8, 'change_permissionextension'),
(31, 'Can delete permission extension', 8, 'delete_permissionextension'),
(32, 'Can view permission extension', 8, 'view_permissionextension'),
(33, 'Can add group extension', 9, 'add_groupextension'),
(34, 'Can change group extension', 9, 'change_groupextension'),
(35, 'Can delete group extension', 9, 'delete_groupextension'),
(36, 'Can view group extension', 9, 'view_groupextension'),
(37, 'Can add organization', 10, 'add_organization'),
(38, 'Can change organization', 10, 'change_organization'),
(39, 'Can delete organization', 10, 'delete_organization'),
(40, 'Can view organization', 10, 'view_organization'),
(41, 'Can add branch', 11, 'add_branch'),
(42, 'Can change branch', 11, 'change_branch'),
(43, 'Can delete branch', 11, 'delete_branch'),
(44, 'Can view branch', 11, 'view_branch'),
(63, 'Can add user profile', 7, 'add_userprofile'),
(62, 'Can view user files', 12, 'view_userfiles'),
(49, 'Can add user files', 12, 'add_userfiles'),
(54, 'saer.pk main head', 10, 'all type'),
(56, 'Can change log entry', 1, 'change_logentry'),
(57, 'Can delete log entry', 1, 'delete_logentry'),
(53, 'sub agent', 10, 'nothhimg'),
(64, 'Can change user profile', 7, 'change_userprofile'),
(65, 'Can delete user profile', 7, 'delete_userprofile'),
(66, 'Can view user profile', 7, 'view_userprofile'),
(67, 'Can add airlines', 13, 'add_airlines'),
(68, 'Can change airlines', 13, 'change_airlines'),
(69, 'Can delete airlines', 13, 'delete_airlines'),
(70, 'Can view airlines', 13, 'view_airlines'),
(71, 'Can add city', 14, 'add_city'),
(72, 'Can change city', 14, 'change_city'),
(73, 'Can delete city', 14, 'delete_city'),
(74, 'Can view city', 14, 'view_city'),
(75, 'Can add shirka', 15, 'add_shirka'),
(76, 'Can change shirka', 15, 'change_shirka'),
(77, 'Can delete shirka', 15, 'delete_shirka'),
(78, 'Can view shirka', 15, 'view_shirka'),
(79, 'Can add transport sector price', 16, 'add_transportsectorprice'),
(80, 'Can change transport sector price', 16, 'change_transportsectorprice'),
(81, 'Can delete transport sector price', 16, 'delete_transportsectorprice'),
(82, 'Can view transport sector price', 16, 'view_transportsectorprice'),
(83, 'Can add umrah visa price', 17, 'add_umrahvisaprice'),
(84, 'Can change umrah visa price', 17, 'change_umrahvisaprice'),
(85, 'Can delete umrah visa price', 17, 'delete_umrahvisaprice'),
(86, 'Can view umrah visa price', 17, 'view_umrahvisaprice'),
(87, 'Can add booking expiry', 18, 'add_bookingexpiry'),
(88, 'Can change booking expiry', 18, 'change_bookingexpiry'),
(89, 'Can delete booking expiry', 18, 'delete_bookingexpiry'),
(90, 'Can view booking expiry', 18, 'view_bookingexpiry'),
(91, 'Can add riyal rate', 19, 'add_riyalrate'),
(92, 'Can change riyal rate', 19, 'change_riyalrate'),
(93, 'Can delete riyal rate', 19, 'delete_riyalrate'),
(94, 'Can view riyal rate', 19, 'view_riyalrate'),
(95, 'Can add ticker stopover details', 20, 'add_tickerstopoverdetails'),
(96, 'Can change ticker stopover details', 20, 'change_tickerstopoverdetails'),
(97, 'Can delete ticker stopover details', 20, 'delete_tickerstopoverdetails'),
(98, 'Can view ticker stopover details', 20, 'view_tickerstopoverdetails'),
(99, 'Can add hotel prices', 21, 'add_hotelprices'),
(100, 'Can change hotel prices', 21, 'change_hotelprices'),
(101, 'Can delete hotel prices', 21, 'delete_hotelprices'),
(102, 'Can view hotel prices', 21, 'view_hotelprices'),
(103, 'Can add ticket trip details', 22, 'add_tickettripdetails'),
(104, 'Can change ticket trip details', 22, 'change_tickettripdetails'),
(105, 'Can delete ticket trip details', 22, 'delete_tickettripdetails'),
(106, 'Can view ticket trip details', 22, 'view_tickettripdetails'),
(107, 'Can add ticket', 23, 'add_ticket'),
(108, 'Can change ticket', 23, 'change_ticket'),
(109, 'Can delete ticket', 23, 'delete_ticket'),
(110, 'Can view ticket', 23, 'view_ticket'),
(111, 'Can add hotels', 24, 'add_hotels'),
(112, 'Can change hotels', 24, 'change_hotels'),
(113, 'Can delete hotels', 24, 'delete_hotels'),
(114, 'Can view hotels', 24, 'view_hotels'),
(115, 'Can add umrah package', 25, 'add_umrahpackage'),
(116, 'Can change umrah package', 25, 'change_umrahpackage'),
(117, 'Can delete umrah package', 25, 'delete_umrahpackage'),
(118, 'Can view umrah package', 25, 'view_umrahpackage'),
(119, 'Can add umrah package transport details', 26, 'add_umrahpackagetransportdetails'),
(120, 'Can change umrah package transport details', 26, 'change_umrahpackagetransportdetails'),
(121, 'Can delete umrah package transport details', 26, 'delete_umrahpackagetransportdetails'),
(122, 'Can view umrah package transport details', 26, 'view_umrahpackagetransportdetails'),
(123, 'Can add umrah package ticket details', 27, 'add_umrahpackageticketdetails'),
(124, 'Can change umrah package ticket details', 27, 'change_umrahpackageticketdetails'),
(125, 'Can delete umrah package ticket details', 27, 'delete_umrahpackageticketdetails'),
(126, 'Can view umrah package ticket details', 27, 'view_umrahpackageticketdetails'),
(127, 'Can add umrah package hotel details', 28, 'add_umrahpackagehoteldetails'),
(128, 'Can change umrah package hotel details', 28, 'change_umrahpackagehoteldetails'),
(129, 'Can delete umrah package hotel details', 28, 'delete_umrahpackagehoteldetails'),
(130, 'Can view umrah package hotel details', 28, 'view_umrahpackagehoteldetails'),
(131, 'Can add agency', 29, 'add_agency'),
(132, 'Can change agency', 29, 'change_agency'),
(133, 'Can delete agency', 29, 'delete_agency'),
(134, 'Can view agency', 29, 'view_agency'),
(135, 'Can add umrah package discount details', 30, 'add_umrahpackagediscountdetails'),
(136, 'Can change umrah package discount details', 30, 'change_umrahpackagediscountdetails'),
(137, 'Can delete umrah package discount details', 30, 'delete_umrahpackagediscountdetails'),
(138, 'Can view umrah package discount details', 30, 'view_umrahpackagediscountdetails'),
(139, 'Can add custom umrah package', 31, 'add_customumrahpackage'),
(140, 'Can change custom umrah package', 31, 'change_customumrahpackage'),
(141, 'Can delete custom umrah package', 31, 'delete_customumrahpackage'),
(142, 'Can view custom umrah package', 31, 'view_customumrahpackage'),
(143, 'Can add umrah visa price two', 32, 'add_umrahvisapricetwo'),
(144, 'Can change umrah visa price two', 32, 'change_umrahvisapricetwo'),
(145, 'Can delete umrah visa price two', 32, 'delete_umrahvisapricetwo'),
(146, 'Can view umrah visa price two', 32, 'view_umrahvisapricetwo'),
(147, 'Can add umrah visa price two hotel', 33, 'add_umrahvisapricetwohotel'),
(148, 'Can change umrah visa price two hotel', 33, 'change_umrahvisapricetwohotel'),
(149, 'Can delete umrah visa price two hotel', 33, 'delete_umrahvisapricetwohotel'),
(150, 'Can view umrah visa price two hotel', 33, 'view_umrahvisapricetwohotel'),
(151, 'Can add custom umrah package transport details', 34, 'add_customumrahpackagetransportdetails'),
(152, 'Can change custom umrah package transport details', 34, 'change_customumrahpackagetransportdetails'),
(153, 'Can delete custom umrah package transport details', 34, 'delete_customumrahpackagetransportdetails'),
(154, 'Can view custom umrah package transport details', 34, 'view_customumrahpackagetransportdetails'),
(155, 'Can add custom umrah package ticket details', 35, 'add_customumrahpackageticketdetails'),
(156, 'Can change custom umrah package ticket details', 35, 'change_customumrahpackageticketdetails'),
(157, 'Can delete custom umrah package ticket details', 35, 'delete_customumrahpackageticketdetails'),
(158, 'Can view custom umrah package ticket details', 35, 'view_customumrahpackageticketdetails'),
(159, 'Can add custom umrah package hotel details', 36, 'add_customumrahpackagehoteldetails'),
(160, 'Can change custom umrah package hotel details', 36, 'change_customumrahpackagehoteldetails'),
(161, 'Can delete custom umrah package hotel details', 36, 'delete_customumrahpackagehoteldetails'),
(162, 'Can view custom umrah package hotel details', 36, 'view_customumrahpackagehoteldetails'),
(163, 'Can add only visa price', 37, 'add_onlyvisaprice'),
(164, 'Can change only visa price', 37, 'change_onlyvisaprice'),
(165, 'Can delete only visa price', 37, 'delete_onlyvisaprice'),
(166, 'Can view only visa price', 37, 'view_onlyvisaprice'),
(167, 'Can add booking', 38, 'add_booking'),
(168, 'Can change booking', 38, 'change_booking'),
(169, 'Can delete booking', 38, 'delete_booking'),
(170, 'Can view booking', 38, 'view_booking'),
(171, 'Can add booking detail', 39, 'add_bookingdetail'),
(172, 'Can change booking detail', 39, 'change_bookingdetail'),
(173, 'Can delete booking detail', 39, 'delete_bookingdetail'),
(174, 'Can view booking detail', 39, 'view_bookingdetail'),
(175, 'Can add agency files', 40, 'add_agencyfiles'),
(176, 'Can change agency files', 40, 'change_agencyfiles'),
(177, 'Can delete agency files', 40, 'delete_agencyfiles'),
(178, 'Can view agency files', 40, 'view_agencyfiles'),
(179, 'Can add agency contact', 41, 'add_agencycontact'),
(180, 'Can change agency contact', 41, 'change_agencycontact'),
(181, 'Can delete agency contact', 41, 'delete_agencycontact'),
(182, 'Can view agency contact', 41, 'view_agencycontact'),
(183, 'Can add set visa type', 42, 'add_setvisatype'),
(184, 'Can change set visa type', 42, 'change_setvisatype'),
(185, 'Can delete set visa type', 42, 'delete_setvisatype'),
(186, 'Can view set visa type', 42, 'view_setvisatype'),
(187, 'Can add ziarat price', 43, 'add_ziaratprice'),
(188, 'Can change ziarat price', 43, 'change_ziaratprice'),
(189, 'Can delete ziarat price', 43, 'delete_ziaratprice'),
(190, 'Can view ziarat price', 43, 'view_ziaratprice'),
(191, 'Can add food price', 44, 'add_foodprice'),
(192, 'Can change food price', 44, 'change_foodprice'),
(193, 'Can delete food price', 44, 'delete_foodprice'),
(194, 'Can view food price', 44, 'view_foodprice'),
(195, 'Can add hotel contact details', 45, 'add_hotelcontactdetails'),
(196, 'Can change hotel contact details', 45, 'change_hotelcontactdetails'),
(197, 'Can delete hotel contact details', 45, 'delete_hotelcontactdetails'),
(198, 'Can view hotel contact details', 45, 'view_hotelcontactdetails'),
(199, 'Can add hotel rooms', 46, 'add_hotelrooms'),
(200, 'Can change hotel rooms', 46, 'change_hotelrooms'),
(201, 'Can delete hotel rooms', 46, 'delete_hotelrooms'),
(202, 'Can view hotel rooms', 46, 'view_hotelrooms'),
(203, 'Can add room details', 47, 'add_roomdetails'),
(204, 'Can change room details', 47, 'change_roomdetails'),
(205, 'Can delete room details', 47, 'delete_roomdetails'),
(206, 'Can view room details', 47, 'view_roomdetails'),
(207, 'Can add custom umrah food details', 48, 'add_customumrahfooddetails'),
(208, 'Can change custom umrah food details', 48, 'change_customumrahfooddetails'),
(209, 'Can delete custom umrah food details', 48, 'delete_customumrahfooddetails'),
(210, 'Can view custom umrah food details', 48, 'view_customumrahfooddetails'),
(211, 'Can add custom umrah ziarat details', 49, 'add_customumrahziaratdetails'),
(212, 'Can change custom umrah ziarat details', 49, 'change_customumrahziaratdetails'),
(213, 'Can delete custom umrah ziarat details', 49, 'delete_customumrahziaratdetails'),
(214, 'Can view custom umrah ziarat details', 49, 'view_customumrahziaratdetails'),
(215, 'Can add bank', 50, 'add_bank'),
(216, 'Can change bank', 50, 'change_bank'),
(217, 'Can delete bank', 50, 'delete_bank'),
(218, 'Can view bank', 50, 'view_bank'),
(219, 'Can add booking hotel details', 51, 'add_bookinghoteldetails'),
(220, 'Can change booking hotel details', 51, 'change_bookinghoteldetails'),
(221, 'Can delete booking hotel details', 51, 'delete_bookinghoteldetails'),
(222, 'Can view booking hotel details', 51, 'view_bookinghoteldetails'),
(223, 'Can add booking person detail', 52, 'add_bookingpersondetail'),
(224, 'Can change booking person detail', 52, 'change_bookingpersondetail'),
(225, 'Can delete booking person detail', 52, 'delete_bookingpersondetail'),
(226, 'Can view booking person detail', 52, 'view_bookingpersondetail'),
(227, 'Can add booking ticket details', 53, 'add_bookingticketdetails'),
(228, 'Can change booking ticket details', 53, 'change_bookingticketdetails'),
(229, 'Can delete booking ticket details', 53, 'delete_bookingticketdetails'),
(230, 'Can view booking ticket details', 53, 'view_bookingticketdetails'),
(231, 'Can add booking ticket stopover details', 54, 'add_bookingticketstopoverdetails'),
(232, 'Can change booking ticket stopover details', 54, 'change_bookingticketstopoverdetails'),
(233, 'Can delete booking ticket stopover details', 54, 'delete_bookingticketstopoverdetails'),
(234, 'Can view booking ticket stopover details', 54, 'view_bookingticketstopoverdetails'),
(235, 'Can add booking ticket ticket trip details', 55, 'add_bookingtickettickettripdetails'),
(236, 'Can change booking ticket ticket trip details', 55, 'change_bookingtickettickettripdetails'),
(237, 'Can delete booking ticket ticket trip details', 55, 'delete_bookingtickettickettripdetails'),
(238, 'Can view booking ticket ticket trip details', 55, 'view_bookingtickettickettripdetails'),
(239, 'Can add booking transport details', 56, 'add_bookingtransportdetails'),
(240, 'Can change booking transport details', 56, 'change_bookingtransportdetails'),
(241, 'Can delete booking transport details', 56, 'delete_bookingtransportdetails'),
(242, 'Can view booking transport details', 56, 'view_bookingtransportdetails'),
(243, 'Can add payment', 57, 'add_payment'),
(244, 'Can change payment', 57, 'change_payment'),
(245, 'Can delete payment', 57, 'delete_payment'),
(246, 'Can view payment', 57, 'view_payment'),
(247, 'Can add booking person ziyarat details', 58, 'add_bookingpersonziyaratdetails'),
(248, 'Can change booking person ziyarat details', 58, 'change_bookingpersonziyaratdetails'),
(249, 'Can delete booking person ziyarat details', 58, 'delete_bookingpersonziyaratdetails'),
(250, 'Can view booking person ziyarat details', 58, 'view_bookingpersonziyaratdetails'),
(251, 'Can add booking person food details', 59, 'add_bookingpersonfooddetails'),
(252, 'Can change booking person food details', 59, 'change_bookingpersonfooddetails'),
(253, 'Can delete booking person food details', 59, 'delete_bookingpersonfooddetails'),
(254, 'Can view booking person food details', 59, 'view_bookingpersonfooddetails'),
(255, 'Can add booking person contact details', 60, 'add_bookingpersoncontactdetails'),
(256, 'Can change booking person contact details', 60, 'change_bookingpersoncontactdetails'),
(257, 'Can delete booking person contact details', 60, 'delete_bookingpersoncontactdetails'),
(258, 'Can view booking person contact details', 60, 'view_bookingpersoncontactdetails'),
(259, 'Can add sector', 61, 'add_sector'),
(260, 'Can change sector', 61, 'change_sector'),
(261, 'Can delete sector', 61, 'delete_sector'),
(262, 'Can view sector', 61, 'view_sector'),
(263, 'Can add big sector', 62, 'add_bigsector'),
(264, 'Can change big sector', 62, 'change_bigsector'),
(265, 'Can delete big sector', 62, 'delete_bigsector'),
(266, 'Can view big sector', 62, 'view_bigsector'),
(267, 'Can add vehicle type', 63, 'add_vehicletype'),
(268, 'Can change vehicle type', 63, 'change_vehicletype'),
(269, 'Can delete vehicle type', 63, 'delete_vehicletype'),
(270, 'Can view vehicle type', 63, 'view_vehicletype'),
(271, 'Can add internal note', 64, 'add_internalnote'),
(272, 'Can change internal note', 64, 'change_internalnote'),
(273, 'Can delete internal note', 64, 'delete_internalnote'),
(274, 'Can view internal note', 64, 'view_internalnote'),
(275, 'Can add booking transport sector', 65, 'add_bookingtransportsector'),
(276, 'Can change booking transport sector', 65, 'change_bookingtransportsector'),
(277, 'Can delete booking transport sector', 65, 'delete_bookingtransportsector'),
(278, 'Can view booking transport sector', 65, 'view_bookingtransportsector'),
(279, 'Can add bank account', 66, 'add_bankaccount'),
(280, 'Can change bank account', 66, 'change_bankaccount'),
(281, 'Can delete bank account', 66, 'delete_bankaccount'),
(282, 'Can view bank account', 66, 'view_bankaccount'),
(283, 'Can add organization link', 67, 'add_organizationlink'),
(284, 'Can change organization link', 67, 'change_organizationlink'),
(285, 'Can delete organization link', 67, 'delete_organizationlink'),
(286, 'Can view organization link', 67, 'view_organizationlink'),
(287, 'Can add allowed reseller', 68, 'add_allowedreseller'),
(288, 'Can change allowed reseller', 68, 'change_allowedreseller'),
(289, 'Can delete allowed reseller', 68, 'delete_allowedreseller'),
(290, 'Can view allowed reseller', 68, 'view_allowedreseller'),
(291, 'Can add discount', 69, 'add_discount'),
(292, 'Can change discount', 69, 'change_discount'),
(293, 'Can delete discount', 69, 'delete_discount'),
(294, 'Can view discount', 69, 'view_discount'),
(295, 'Can add discount group', 70, 'add_discountgroup'),
(296, 'Can change discount group', 70, 'change_discountgroup'),
(297, 'Can delete discount group', 70, 'delete_discountgroup'),
(298, 'Can view discount group', 70, 'view_discountgroup'),
(299, 'Can add markup', 71, 'add_markup'),
(300, 'Can change markup', 71, 'change_markup'),
(301, 'Can delete markup', 71, 'delete_markup'),
(302, 'Can view markup', 71, 'view_markup');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(33, 'pbkdf2_sha256$600000$8Z510T1L0KaLNP3kXF8cJS$L1maDX6kD7Yp5m7lh8...\npbkdf2_sha256$600000$8Z510T1L0KaLNP3kXF8cJS$L1maDX6kD7Yp5m7lh8', NULL, 0, 'mubeen@gmail.com', 'Mubeen', 'Abbas', 'mubeen@gmial.com', 0, 1, '2025-08-31 05:47:41.000000'),
(20, 'pbkdf2_sha256$600000$8Z510T1L0KaLNP3kXF8cJS$L1maDX9wMcEGCzD4qjtpcZfzyB5HCTsgB5ORlVFhEfA=', NULL, 0, 'ahsan@gmail.com', 'Ashan malik', '', 'ahsan@gmail.com', 0, 0, '2025-07-18 11:20:45.161746'),
(21, 'pbkdf2_sha256$600000$Mcd51Cud8L6dYtByo3yd2J$hqpBo7M+zRXJmZdL5mOD0EMQS+kkRVk399UJOHfrTGU=', NULL, 0, 'malik@gmail.com', 'Malik', '', 'malik@gmail.com', 0, 1, '2025-07-18 11:21:24.889353'),
(32, 'pbkdf2_sha256$600000$1pQUmwfHJE5p9dDExVNBEx$aT+WxbSh6nLNYlVsNCbzOSU208dWr6AJStZPP/XRw6Y=', NULL, 0, 'jfsfd@gmail.com', 'Daniyal Abbas', '', 'jfsfd@gmail.com', 0, 1, '2025-08-17 17:46:42.561909'),
(30, 'pbkdf2_sha256$600000$50cuxN3qtnfTmP1bHEMbnd$YFXrh4wVJ7tftpkhqLStPTGvJp0Rzf5eb9lscuFnRj0=', NULL, 0, 'Bilal@gmail.com', 'Ahsan', '', 'ahsaan.raza.butt@gmail.com', 0, 1, '2025-08-04 18:57:42.399640'),
(29, 'pbkdf2_sha256$600000$oSNXTGvsKf7ypjxojypzBQ$+/b7b0OFbMrFLwRRiuCofBhBDyN5+KncHoej/SxQGKI=', NULL, 0, 'new@gmail.com', 'new', '', 'new@gmail.com', 0, 1, '2025-07-19 19:56:49.925496'),
(34, 'pbkdf2_sha256$600000$FVQpwOh1GocCa11DrtMJMc$KlsEOx3BbpjP0+wHlLb3xPTq+m9qJVvKs115Zr9F3V8=', NULL, 0, 'abc@gmail.com', 'Ali', '', 'abc@gmail.com', 0, 1, '2025-08-31 12:55:47.830622');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(40, 24, 21),
(48, 29, 21),
(35, 21, 22),
(39, 20, 22),
(52, 34, 21),
(47, 29, 19),
(51, 32, 21),
(49, 30, 19);

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `big_sector`
--

CREATE TABLE `big_sector` (
  `id` bigint(20) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `big_sector`
--

INSERT INTO `big_sector` (`id`, `organization_id`) VALUES
(19, 8),
(17, 8),
(15, 8),
(20, 8),
(14, 8);

-- --------------------------------------------------------

--
-- Table structure for table `big_sector_small_sectors`
--

CREATE TABLE `big_sector_small_sectors` (
  `id` bigint(20) NOT NULL,
  `bigsector_id` bigint(20) NOT NULL,
  `sector_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `big_sector_small_sectors`
--

INSERT INTO `big_sector_small_sectors` (`id`, `bigsector_id`, `sector_id`) VALUES
(25, 15, 10),
(24, 14, 7),
(21, 14, 9),
(23, 14, 8),
(22, 14, 10),
(26, 15, 7),
(37, 20, 9),
(38, 20, 10),
(29, 17, 8),
(30, 17, 7),
(39, 20, 6),
(36, 19, 9),
(35, 19, 8);

-- --------------------------------------------------------

--
-- Table structure for table `booking_allowedreseller`
--

CREATE TABLE `booking_allowedreseller` (
  `id` bigint(20) NOT NULL,
  `allowed` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`allowed`)),
  `requested_status_by_reseller` varchar(20) NOT NULL,
  `commission_group_id` int(11) DEFAULT NULL,
  `markup_group_id` int(11) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `inventory_owner_company_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_allowedreseller`
--

INSERT INTO `booking_allowedreseller` (`id`, `allowed`, `requested_status_by_reseller`, `commission_group_id`, `markup_group_id`, `created_at`, `updated_at`, `inventory_owner_company_id`) VALUES
(1, '[\"UMRAH_PACKAGES\", \"HOTELS\"]', 'PENDING', 10, 5, '2025-09-27 16:00:34.335013', '2025-09-27 16:00:34.335113', 1);

-- --------------------------------------------------------

--
-- Table structure for table `booking_allowedreseller_reseller_companies`
--

CREATE TABLE `booking_allowedreseller_reseller_companies` (
  `id` bigint(20) NOT NULL,
  `allowedreseller_id` bigint(20) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_allowedreseller_reseller_companies`
--

INSERT INTO `booking_allowedreseller_reseller_companies` (`id`, `allowedreseller_id`, `organization_id`) VALUES
(1, 1, 8);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bank`
--

CREATE TABLE `booking_bank` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `account_title` varchar(100) DEFAULT NULL,
  `account_number` longtext DEFAULT NULL,
  `iban` varchar(50) DEFAULT NULL,
  `organization_id` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `booking_bankaccount`
--

CREATE TABLE `booking_bankaccount` (
  `id` bigint(20) NOT NULL,
  `bank_name` varchar(255) NOT NULL,
  `account_title` varchar(255) NOT NULL,
  `account_number` varchar(50) NOT NULL,
  `iban` varchar(34) NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `agency_id` bigint(20) DEFAULT NULL,
  `branch_id` bigint(20) DEFAULT NULL,
  `organization_id` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bankaccount`
--

INSERT INTO `booking_bankaccount` (`id`, `bank_name`, `account_title`, `account_number`, `iban`, `status`, `created_at`, `updated_at`, `agency_id`, `branch_id`, `organization_id`) VALUES
(1, 'Habib Bank Limited', 'Usama Jameel', '1234567890', 'PK36HABB0000123456789002', 'active', '2025-09-23 12:29:18.366208', '2025-09-23 12:29:18.366299', 6, 14, 8);

-- --------------------------------------------------------

--
-- Table structure for table `booking_booking`
--

CREATE TABLE `booking_booking` (
  `id` bigint(20) NOT NULL,
  `booking_number` varchar(20) NOT NULL,
  `date` datetime(6) NOT NULL,
  `total_amount` double NOT NULL,
  `is_paid` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `agency_id` bigint(20) NOT NULL,
  `branch_id` bigint(20) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `total_hotel_amount` double NOT NULL,
  `total_pax` int(11) NOT NULL,
  `total_ticket_amount` double NOT NULL,
  `total_transport_amount` double NOT NULL,
  `total_visa_amount` double NOT NULL,
  `is_partial_payment_allowed` tinyint(1) NOT NULL,
  `total_adult` int(11) NOT NULL,
  `total_child` int(11) NOT NULL,
  `total_infant` int(11) NOT NULL,
  `expiry_time` datetime(6) DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `rejected_notes` longtext DEFAULT NULL,
  `rejected_at` datetime(6) DEFAULT NULL,
  `call_status` tinyint(1) NOT NULL,
  `client_note` longtext DEFAULT NULL,
  `paid_payment` double DEFAULT NULL,
  `pending_payment` double DEFAULT NULL,
  `total_food_amount_pkr` double DEFAULT NULL,
  `total_food_amount_sar` double DEFAULT NULL,
  `total_hotel_amount_pkr` double DEFAULT NULL,
  `total_hotel_amount_sar` double DEFAULT NULL,
  `total_in_pkr` double DEFAULT NULL,
  `total_ticket_amount_pkr` double DEFAULT NULL,
  `total_transport_amount_pkr` double DEFAULT NULL,
  `total_transport_amount_sar` double DEFAULT NULL,
  `total_visa_amount_pkr` double DEFAULT NULL,
  `total_visa_amount_sar` double DEFAULT NULL,
  `total_ziyarat_amount_pkr` double DEFAULT NULL,
  `total_ziyarat_amount_sar` double DEFAULT NULL,
  `umrah_package_id` bigint(20) DEFAULT NULL,
  `is_visa_price_pkr` tinyint(1) NOT NULL,
  `visa_rate` double DEFAULT NULL,
  `visa_rate_in_pkr` double DEFAULT NULL,
  `visa_rate_in_sar` double DEFAULT NULL,
  `visa_riyal_rate` double DEFAULT NULL,
  `is_food_included` tinyint(1) NOT NULL,
  `is_ziyarat_included` tinyint(1) NOT NULL,
  `rejected_employer_id` int(11) DEFAULT NULL,
  `confirmed_by_id` int(11) DEFAULT NULL,
  `owner_organization_id` int(11) DEFAULT NULL,
  `selling_organization_id` int(11) DEFAULT NULL,
  `booking_organization_id` int(11) DEFAULT NULL,
  `inventory_owner_organization_id` int(11) DEFAULT NULL,
  `markup_by_reseller` double DEFAULT NULL,
  `reseller_commission` double DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_booking`
--

INSERT INTO `booking_booking` (`id`, `booking_number`, `date`, `total_amount`, `is_paid`, `status`, `agency_id`, `branch_id`, `organization_id`, `user_id`, `payment_status`, `total_hotel_amount`, `total_pax`, `total_ticket_amount`, `total_transport_amount`, `total_visa_amount`, `is_partial_payment_allowed`, `total_adult`, `total_child`, `total_infant`, `expiry_time`, `category`, `created_at`, `action`, `rejected_notes`, `rejected_at`, `call_status`, `client_note`, `paid_payment`, `pending_payment`, `total_food_amount_pkr`, `total_food_amount_sar`, `total_hotel_amount_pkr`, `total_hotel_amount_sar`, `total_in_pkr`, `total_ticket_amount_pkr`, `total_transport_amount_pkr`, `total_transport_amount_sar`, `total_visa_amount_pkr`, `total_visa_amount_sar`, `total_ziyarat_amount_pkr`, `total_ziyarat_amount_sar`, `umrah_package_id`, `is_visa_price_pkr`, `visa_rate`, `visa_rate_in_pkr`, `visa_rate_in_sar`, `visa_riyal_rate`, `is_food_included`, `is_ziyarat_included`, `rejected_employer_id`, `confirmed_by_id`, `owner_organization_id`, `selling_organization_id`, `booking_organization_id`, `inventory_owner_organization_id`, `markup_by_reseller`, `reseller_commission`) VALUES
(1, 'UMRAH-NaN', '2025-08-22 16:34:28.157399', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 05:34:26.331000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(2, 'UMRAH-N', '2025-08-22 17:17:24.092634', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 06:17:22.001000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(3, 'UMRAH-NaN', '2025-08-23 03:59:49.075639', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 16:59:46.314000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(4, 'UMRAH-NaN', '2025-08-23 04:06:18.440129', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 17:06:17.509000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(5, 'UMRAH-N', '2025-08-23 04:11:48.843961', 140054, 1, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 17:11:47.905000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(6, 'UMRAH-NaN', '2025-08-23 05:50:10.729881', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 18:50:09.582000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(7, 'UMRAH-NaN', '2025-08-23 06:07:29.902255', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 19:07:27.473000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(8, 'UMRAH-NaN', '2025-08-23 06:11:04.101923', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 19:11:01.497000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(9, 'UMRAH-NaN', '2025-08-23 06:27:45.245043', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 110002, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 19:27:43.998000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(10, '1', '2025-08-23 06:31:28.584828', 0, 0, 'ok', 10, 19, 8, 29, 'Pending', 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(11, 'UMRAH-Na', '2025-08-23 08:11:03.264162', 140054, 1, 'under-process', 10, 19, 8, 29, 'PENDING', 0, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 21:10:21.118000', 'Package', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(12, 'UMRAH-NaN', '2025-08-23 08:15:03.233257', 112053, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 0, 1, 10000, 50, 1000, 1, 0, 1, 0, '2025-08-27 21:14:16.344000', 'Package', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(13, 'UMRAH-NaN', '2025-08-23 08:16:20.834917', 140054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 0, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 21:15:37.746000', 'Package', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(14, 'UMRAH-NaN', '2025-08-23 08:18:57.502868', 140054, 1, 'un-approve', 10, 19, 8, 29, 'PENDING', 0, 1, 20000, 50, 10000, 1, 1, 0, 0, '2025-08-27 21:18:08.407000', 'Package', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(15, '1', '2025-08-23 08:28:02.821560', 0, 0, 'ok', 10, 19, 8, 29, 'Pending', 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(16, '1', '2025-08-23 08:28:55.871867', 0, 0, 'ok', 10, 19, 8, 29, 'Pending', 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(17, 'BKMEPIZGYCI0DHHL', '2025-08-24 10:08:27.098885', 20000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 20000, 0, 0, 0, 1, 0, 0, '2025-08-28 23:08:25.236000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(18, 'BKMEPJSM4FC4SFHN', '2025-08-24 10:31:06.496700', 0, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 0, 0, 0, 0, 1, 0, 0, '2025-08-28 23:31:04.959000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(19, 'BKMEPK6Y92ZLTNH2', '2025-08-24 10:42:15.574923', 0, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 0, 0, 0, 0, 1, 0, 0, '2025-08-28 23:42:13.862000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(20, 'BKMES6U44GVCRULR', '2025-08-26 06:51:38.857751', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-08-30 19:51:38.464000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(21, 'BKMES6XMAXR8AVIL', '2025-08-26 06:54:22.643918', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-08-30 19:54:21.993000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(22, 'UMRAH-NaN', '2025-08-26 07:13:21.095324', 340054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-08-30 20:13:19.162000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(23, 'UMRAH-1', '2025-08-26 07:19:30.422076', 340054, 0, 'Pending', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-08-27 07:19:30.195000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(24, 'BKMETM92OEEXSA7U', '2025-08-27 06:50:58.250250', 120000, 1, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-08-31 19:50:56.846000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(25, 'BKMEUXGAZLQA5S4X', '2025-08-28 04:52:17.235744', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 17:52:16.161000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(26, 'BKMEUXH0TFUJ9YO1', '2025-08-28 04:52:50.834538', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 17:52:49.635000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(27, 'BKMEUXTCEPQVTK7P', '2025-08-28 05:02:25.764796', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 18:02:24.529000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(28, 'BKMEUY1VOJU2VOG2', '2025-08-28 05:09:04.030237', 0, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 0, 0, 0, 0, 1, 0, 0, '2025-09-01 18:09:02.755000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(29, 'BKMEUY24VP54INYZ', '2025-08-28 05:09:15.520175', 0, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 0, 0, 0, 0, 1, 0, 0, '2025-09-01 18:09:14.677000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(30, 'BKMEUY4F2FGCKM1C', '2025-08-28 05:11:02.501277', 0, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 0, 0, 0, 0, 1, 0, 0, '2025-09-01 18:11:01.191000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(31, 'BKMEV5PCKWQ9FFD9', '2025-08-28 08:43:16.972133', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 21:43:15.056000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(32, 'BKMEV6GT90TZKB97', '2025-08-28 09:04:37.755427', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:04:36.372000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(33, 'BKMEV6YE1EHO1KJN', '2025-08-28 09:18:17.879247', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(34, 'BKMEV6YE1EHO1KJN', '2025-08-28 10:29:44.641052', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(35, 'BKMEV6YE1EHO1KJN', '2025-08-28 11:15:12.005281', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(36, 'BKMEV6YE1EHO1KJN', '2025-08-28 11:41:04.676527', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(37, 'BKMEV6YE1EHO1KJN', '2025-08-28 11:57:44.997686', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(38, 'BKMEV6YE1EHO1KJN', '2025-08-28 11:58:07.318742', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(39, 'BKMEV6YE1EHO1KJN', '2025-08-28 11:58:07.327233', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(40, 'BKMEV6YE1EHO1KJN', '2025-08-28 12:25:19.272700', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-01 22:18:16.466000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(41, 'BKMEWCUDEJSNWYXT', '2025-08-29 04:50:54.475375', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-02 17:50:52.891000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(42, 'UMRAH-NaN', '2025-08-29 18:17:50.227816', 340054, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-09-03 07:17:46.538000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(43, 'UMRAH-NaN', '2025-08-29 18:22:32.279464', 340054, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-09-03 07:22:28.942000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(44, 'UMRAH-NaN', '2025-08-29 18:24:01.509307', 340054, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-09-03 07:23:58.179000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(45, 'UMRAH-1', '2025-08-29 18:26:34.234040', 340054, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-09-03 07:26:30.822000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(46, 'UMRAH-NaN', '2025-08-29 18:33:24.352215', 63, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 9, 1, 0, 50, 1, 1, 1, 0, 0, '2025-09-03 07:33:21.909000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(47, 'UMRAH-NaN', '2025-08-29 18:37:03.013114', 63, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 9, 1, 0, 50, 1, 1, 1, 0, 0, '2025-09-03 07:36:57.822000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(48, 'UMRAH-NaN', '2025-08-30 06:07:21.824857', 340054, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-09-03 19:07:18.170000', NULL, '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(49, 'UMRAH-NaN', '2025-08-30 19:32:32.087714', 340054, 0, 'Package Booking', 10, 19, 8, 29, 'PENDING', 210002, 1, 120000, 50, 10000, 1, 1, 0, 0, '2025-09-04 08:32:29.627000', 'Package', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(50, 'BKMEZQM2UEK726CT', '2025-08-31 13:39:41.016847', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-05 02:39:39.110000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(51, 'BKMF6UHJ271Z2DP3', '2025-09-05 13:02:29.378337', 120000, 0, 'Pending', 10, 19, 8, 29, 'Pending', 0, 1, 120000, 0, 0, 0, 1, 0, 0, '2025-09-10 02:02:28.543000', 'Ticket_Booking', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(52, 'string', '2025-09-13 15:44:29.740256', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(53, 'BK-20250913-FC02E6', '2025-09-13 16:19:30.902568', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(54, 'string', '2025-09-13 18:40:36.316463', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(55, 'BK-20250913-36D372', '2025-09-13 18:50:46.776351', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(56, 'BK-20250914-69520F', '2025-09-14 12:33:09.176435', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(57, 'BK-20250914-8A9A04', '2025-09-14 12:45:31.913940', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(58, 'BK-20250914-9BAD30', '2025-09-14 12:48:08.181648', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(59, 'BK-20250914-B8A36C', '2025-09-14 12:48:10.116159', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(60, 'BK-20250914-CBADC1', '2025-09-14 12:49:37.506033', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(61, 'BK-20250914-A05FD6', '2025-09-14 12:51:59.493222', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(62, 'BK-20250914-162F53', '2025-09-14 12:53:03.499198', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(63, 'BK-20250914-028983', '2025-09-14 12:53:27.198837', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(64, 'BK-20250914-BC117E', '2025-09-14 12:55:59.499326', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(65, 'BK-20250914-A243BF', '2025-09-14 12:57:44.385906', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(66, 'BK-20250914-0CE38B', '2025-09-14 12:57:47.533874', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(67, 'BK-20250914-9E4C79', '2025-09-14 12:59:54.144587', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(68, 'BK-20250914-8DE801', '2025-09-14 13:01:21.089641', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(69, 'BK-20250914-80CE41', '2025-09-14 13:03:00.288675', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(70, 'BK-20250914-5502C9', '2025-09-14 13:05:44.502708', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(71, 'BK-20250915-ACF791', '2025-09-15 16:42:12.901973', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(72, 'BK-20250915-DABB11', '2025-09-15 16:42:39.050650', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(73, 'BK-20250915-DD0F65', '2025-09-15 16:43:56.748676', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(74, 'BK-20250915-DD541D', '2025-09-15 16:45:06.664394', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(75, 'BK-20250915-5066CD', '2025-09-15 16:45:45.037812', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(76, 'BK-20250915-82BB54', '2025-09-15 17:58:09.732272', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(77, 'BK-20250915-CE8987', '2025-09-15 18:11:29.512081', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(78, 'BK-20250915-C3368A', '2025-09-15 18:15:09.715672', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(79, 'BK-20250915-2E5D7B', '2025-09-15 18:23:09.091136', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(80, 'BK-20250915-958350', '2025-09-15 18:23:36.171025', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(81, 'BK-20250915-8621ED', '2025-09-15 18:23:56.437974', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(82, 'BK-20250915-36B03D', '2025-09-15 18:24:47.718281', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(83, 'BK-20250917-1230D1', '2025-09-17 19:39:19.305399', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(84, 'BK-20250917-DA597F', '2025-09-17 19:42:03.130192', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(85, 'BK-20250917-1A15E7', '2025-09-17 19:42:27.838194', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(86, 'BK-20250917-453A09', '2025-09-17 19:43:13.465534', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(87, 'BK-20250918-A3DC74', '2025-09-18 12:08:33.609605', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(88, 'BK-20250918-629D03', '2025-09-18 12:09:09.381957', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(89, 'BK-20250918-A50365', '2025-09-18 12:11:24.002171', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-18 19:29:39.552445', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(90, 'BK-20250919-DF948B', '2025-09-19 10:09:21.984136', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-19 10:09:21.984261', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(91, 'BK-20250919-7F9DFB', '2025-09-19 10:22:59.815051', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-19 10:22:59.815319', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(92, 'BK-20250919-6BDB9E', '2025-09-19 10:26:32.726275', 3489.5660826720887, 0, 'string', 10, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-19 10:26:32.726500', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(93, 'BK-20250919-80F07E', '2025-09-19 10:41:15.534365', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-19 10:41:15.534519', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(94, 'BK-20250919-67FBED', '2025-09-19 10:43:41.138398', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-19 10:43:41.138586', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(95, 'BK-20250919-B7AA6E', '2025-09-19 10:44:02.835805', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-19 10:44:02.835992', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(96, 'BK-20250920-82B59D', '2025-09-20 14:28:45.626465', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:28:45.626644', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(97, 'BK-20250920-C2062F', '2025-09-20 14:30:47.125766', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:30:47.125971', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(98, 'BK-20250920-9EBD4E', '2025-09-20 14:31:01.231705', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:31:01.231839', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(99, 'BK-20250920-5AD11B', '2025-09-20 14:35:02.867729', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:35:02.867900', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(100, 'BK-20250920-66B787', '2025-09-20 14:40:31.448227', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:40:31.448457', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(101, 'BK-20250920-EBBF4C', '2025-09-20 14:41:01.435979', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:41:01.436143', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(102, 'BK-20250920-DF01BF', '2025-09-20 14:49:56.725312', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:49:56.725574', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(103, 'BK-20250920-5C5D22', '2025-09-20 14:50:21.800959', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:50:21.801200', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(104, 'BK-20250920-F8B329', '2025-09-20 14:56:52.307489', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:56:52.307746', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(105, 'BK-20250920-A306E3', '2025-09-20 14:57:58.697749', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:57:58.697974', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(106, 'BK-20250920-4685D0', '2025-09-20 14:59:00.434352', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 14:59:00.434545', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(107, 'BK-20250920-EC8F0B', '2025-09-20 15:01:51.895484', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 15:01:51.895860', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(108, 'BK-20250920-914D4F', '2025-09-20 15:02:48.910287', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 15:02:48.910518', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(109, 'BK-20250920-051D1B', '2025-09-20 15:03:20.977352', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 15:03:20.977505', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(110, 'BK-20250920-F24C34', '2025-09-20 15:05:08.644043', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 15:05:08.644281', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(111, 'BK-20250920-B4CB3A', '2025-09-20 15:07:05.038755', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 15:07:05.039017', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0),
(112, 'BK-20250920-B184D0', '2025-09-20 15:11:30.935258', 3489.5660826720887, 0, 'string', 6, 19, 8, 33, 'string', 6274.186176975938, -148541304, 2467.0336665214786, 5252.287979682149, 6002.966990704628, 0, -677805131, -1044518737, 589404565, '2019-09-01 23:03:13.907000', 'string', '2025-09-20 15:11:30.935473', NULL, NULL, NULL, 0, NULL, 0, 0, 0, 0, 650000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, NULL, 33, NULL, NULL, NULL, NULL, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookinghoteldetails`
--

CREATE TABLE `booking_bookinghoteldetails` (
  `id` bigint(20) NOT NULL,
  `check_in_date` date DEFAULT NULL,
  `check_out_date` date DEFAULT NULL,
  `number_of_nights` int(11) NOT NULL,
  `room_type` varchar(20) DEFAULT NULL,
  `price` double NOT NULL,
  `quantity` double NOT NULL,
  `total_price` double NOT NULL,
  `booking_id` bigint(20) NOT NULL,
  `hotel_id` bigint(20) NOT NULL,
  `is_price_pkr` tinyint(1) NOT NULL,
  `riyal_rate` double NOT NULL,
  `contact_person_name` varchar(255) DEFAULT NULL,
  `contact_person_number` varchar(20) DEFAULT NULL,
  `check_in_status` varchar(10) NOT NULL,
  `check_out_status` varchar(10) NOT NULL,
  `leg_no` int(10) UNSIGNED NOT NULL CHECK (`leg_no` >= 0),
  `hotel_brn` varchar(100) DEFAULT NULL,
  `hotel_voucher_number` varchar(100) DEFAULT NULL,
  `total_in_pkr` double DEFAULT NULL,
  `total_in_riyal_rate` double DEFAULT NULL,
  `self_hotel_name` varchar(255) DEFAULT NULL,
  `sharing_type` varchar(50) DEFAULT NULL,
  `special_request` longtext DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookinghoteldetails`
--

INSERT INTO `booking_bookinghoteldetails` (`id`, `check_in_date`, `check_out_date`, `number_of_nights`, `room_type`, `price`, `quantity`, `total_price`, `booking_id`, `hotel_id`, `is_price_pkr`, `riyal_rate`, `contact_person_name`, `contact_person_number`, `check_in_status`, `check_out_status`, `leg_no`, `hotel_brn`, `hotel_voucher_number`, `total_in_pkr`, `total_in_riyal_rate`, `self_hotel_name`, `sharing_type`, `special_request`) VALUES
(1, '2025-07-23', '2025-07-31', 8, '', 0, 0, 0, 11, 16, 1, 80, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(2, '2025-08-01', '2025-08-09', 8, '', 0, 0, 0, 11, 13, 1, 80, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(3, '2025-07-23', '2025-07-31', 8, 'Only-Room', 0, 0, 0, 48, 16, 0, 80, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(4, '2025-08-01', '2025-08-09', 8, 'Sharing', 8000, 0, 64000, 48, 13, 0, 80, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(5, NULL, NULL, 0, NULL, 0, 0, 0, 52, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(6, NULL, NULL, 0, NULL, 0, 0, 0, 53, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(7, NULL, NULL, 0, NULL, 0, 0, 0, 54, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(8, NULL, NULL, 0, NULL, 0, 0, 0, 55, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, '2025-09-14', '2025-09-14', 2147483647, 'string', 0, 0, 0, 56, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(10, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 1000, 70, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(11, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 1000, 74, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(12, '2025-10-10', '2025-10-20', 10, 'string', 100, 3, 1000, 75, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(13, '2025-10-10', '2025-10-20', 10, 'string', 100, 3, 3000, 76, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(14, '2025-10-10', '2025-10-20', 10, 'string', 100, 3, 3000, 81, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(15, '2025-10-10', '2025-10-20', 10, 'string', 100, 3, 3000, 82, 19, 1, 0, 'test', '03001234567', 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(16, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 85, 19, 1, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(17, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 86, 19, 0, 0, NULL, NULL, 'inactive', 'inactive', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(18, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 89, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(19, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 90, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(20, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 91, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(21, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 92, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(22, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 93, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(23, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 94, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(24, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 95, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(25, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 96, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(26, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 97, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(27, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 98, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(28, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 99, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(29, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 100, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(30, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 101, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(31, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 102, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(32, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 103, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(33, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 104, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(34, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 105, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(35, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 106, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(36, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 107, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(37, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 108, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(38, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 109, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(39, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 110, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(40, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 111, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL),
(41, '2025-10-10', '2025-10-20', 10, 'string', 100, 10, 10000, 112, 19, 0, 0, NULL, NULL, 'active', 'active', 1, NULL, NULL, 650000, 10000, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingpersoncontactdetails`
--

CREATE TABLE `booking_bookingpersoncontactdetails` (
  `id` bigint(20) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `person_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingpersoncontactdetails`
--

INSERT INTO `booking_bookingpersoncontactdetails` (`id`, `phone_number`, `remarks`, `person_id`) VALUES
(1, '', '', 12),
(2, '', '', 13),
(3, '', '', 15),
(4, '', '', 16);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingpersondetail`
--

CREATE TABLE `booking_bookingpersondetail` (
  `id` bigint(20) NOT NULL,
  `age_group` varchar(20) DEFAULT NULL,
  `person_title` varchar(10) DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `passpoet_issue_date` date DEFAULT NULL,
  `passport_expiry_date` date DEFAULT NULL,
  `passport_picture` varchar(100) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `visa_price` double NOT NULL,
  `is_family_head` tinyint(1) NOT NULL,
  `visa_status` varchar(20) NOT NULL,
  `ticket_status` varchar(20) NOT NULL,
  `ticket_remarks` longtext DEFAULT NULL,
  `booking_id` bigint(20) NOT NULL,
  `shirka_id` bigint(20) DEFAULT NULL,
  `family_number` int(11) NOT NULL,
  `is_visa_included` tinyint(1) NOT NULL,
  `visa_group_number` varchar(20) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `this_pex_remarks` longtext DEFAULT NULL,
  `ticket_discount` double NOT NULL,
  `ticket_price` double NOT NULL,
  `visa_remarks` longtext DEFAULT NULL,
  `is_visa_price_pkr` tinyint(1) NOT NULL,
  `visa_rate` double DEFAULT NULL,
  `visa_rate_in_pkr` double DEFAULT NULL,
  `visa_rate_in_sar` double DEFAULT NULL,
  `visa_riyal_rate` double DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingpersondetail`
--

INSERT INTO `booking_bookingpersondetail` (`id`, `age_group`, `person_title`, `first_name`, `last_name`, `passport_number`, `date_of_birth`, `passpoet_issue_date`, `passport_expiry_date`, `passport_picture`, `country`, `visa_price`, `is_family_head`, `visa_status`, `ticket_status`, `ticket_remarks`, `booking_id`, `shirka_id`, `family_number`, `is_visa_included`, `visa_group_number`, `contact_number`, `this_pex_remarks`, `ticket_discount`, `ticket_price`, `visa_remarks`, `is_visa_price_pkr`, `visa_rate`, `visa_rate_in_pkr`, `visa_rate_in_sar`, `visa_riyal_rate`) VALUES
(1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 1, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 2, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 3, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(4, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 4, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 5, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(6, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 6, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(7, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 9, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(8, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 12, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(9, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 13, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(10, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 14, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(11, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 22, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(12, 'Adult', 'MR', 'Hassan', 'alii', 'jfjsdfh8f8sd', '2006-08-21', '2025-08-28', '2025-09-06', '', 'Pakistan', 0, 0, 'No', 'NOT APPROVED', '', 40, NULL, 0, 0, '', NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(13, 'Adult', 'MR', 'Mubeen', 'Abbas', 'HF7332U', '2006-08-21', '2025-08-28', '2025-09-06', '', 'Pakistan', 0, 0, 'No', 'NOT APPROVED', '', 41, NULL, 0, 0, '', NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(14, 'ADULT', 'MR', 'Ahsan', 'Raza', 'HFU8', '2025-08-30', '2025-08-30', '2025-09-06', 'media/passport_pictures/248286_thumb.jfif', 'Azerbaijan', 10000, 1, 'NOT APPLIED', 'NOT APPROVED', '', 48, NULL, 0, 1, '', NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(15, 'Adult', 'MR', 'AHSAN', 'RAZA', '2468979SD', '2000-10-10', '2000-10-10', '2020-10-10', '', 'Pakistan', 0, 0, 'No', 'NOT APPROVED', '', 50, NULL, 0, 0, '', NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(16, 'Adult', 'MR', 'Abdul Rehman', 'Muzammil', 'kjhgh', '1997-02-13', '2025-09-30', '2025-10-30', '', 'Pakistan', 0, 0, 'No', 'NOT APPROVED', '', 51, NULL, 0, 0, '', NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(17, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 52, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(18, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 53, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(19, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 54, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(20, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 55, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(21, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 56, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(22, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 70, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(23, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 74, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(24, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 75, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(25, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 76, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(26, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 77, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(27, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 78, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(28, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 79, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(29, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 80, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 81, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 82, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(32, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 85, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(33, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 86, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(34, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 87, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(35, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 88, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(36, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 89, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(37, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 90, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(38, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 91, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(39, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 92, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(40, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 93, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(41, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 94, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(42, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 95, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(43, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 99, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(44, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 100, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(45, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 101, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(46, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 102, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(47, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 103, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(48, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 105, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(49, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 106, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(50, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 108, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(51, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 110, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(52, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 111, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0),
(53, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, 0, 0, 'Pending', 'Pending', NULL, 112, NULL, 0, 0, NULL, NULL, NULL, 0, 0, NULL, 1, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingpersonfooddetails`
--

CREATE TABLE `booking_bookingpersonfooddetails` (
  `id` bigint(20) NOT NULL,
  `food` varchar(50) NOT NULL,
  `price` double NOT NULL,
  `is_price_pkr` tinyint(1) NOT NULL,
  `riyal_rate` double NOT NULL,
  `person_id` bigint(20) NOT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `contact_person_name` varchar(100) DEFAULT NULL,
  `food_brn` varchar(100) DEFAULT NULL,
  `food_voucher_number` varchar(100) DEFAULT NULL,
  `per_pax_price` double NOT NULL,
  `price_in_sar` double NOT NULL,
  `total_pax` int(11) NOT NULL,
  `total_price` double NOT NULL,
  `total_price_in_pkr` double NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingpersonfooddetails`
--

INSERT INTO `booking_bookingpersonfooddetails` (`id`, `food`, `price`, `is_price_pkr`, `riyal_rate`, `person_id`, `contact_number`, `contact_person_name`, `food_brn`, `food_voucher_number`, `per_pax_price`, `price_in_sar`, `total_pax`, `total_price`, `total_price_in_pkr`) VALUES
(1, 'no', 1, 1, 80, 14, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingpersonziyaratdetails`
--

CREATE TABLE `booking_bookingpersonziyaratdetails` (
  `id` bigint(20) NOT NULL,
  `city` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `price` double NOT NULL,
  `is_price_pkr` tinyint(1) NOT NULL,
  `riyal_rate` double NOT NULL,
  `person_id` bigint(20) NOT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `contact_person_name` varchar(100) DEFAULT NULL,
  `per_pax_price` double NOT NULL,
  `price_in_sar` double NOT NULL,
  `total_pax` int(11) NOT NULL,
  `total_price` double NOT NULL,
  `total_price_in_pkr` double NOT NULL,
  `ziyarar_voucher_number` varchar(100) DEFAULT NULL,
  `ziyarat_brn` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingpersonziyaratdetails`
--

INSERT INTO `booking_bookingpersonziyaratdetails` (`id`, `city`, `date`, `price`, `is_price_pkr`, `riyal_rate`, `person_id`, `contact_number`, `contact_person_name`, `per_pax_price`, `price_in_sar`, `total_pax`, `total_price`, `total_price_in_pkr`, `ziyarar_voucher_number`, `ziyarat_brn`) VALUES
(1, 'no', '2025-08-30', 1, 0, 80, 14, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingticketdetails`
--

CREATE TABLE `booking_bookingticketdetails` (
  `id` bigint(20) NOT NULL,
  `is_meal_included` tinyint(1) NOT NULL,
  `is_refundable` tinyint(1) NOT NULL,
  `pnr` varchar(100) NOT NULL,
  `child_price` double NOT NULL,
  `infant_price` double NOT NULL,
  `adult_price` double NOT NULL,
  `seats` int(11) NOT NULL,
  `weight` double NOT NULL,
  `pieces` int(11) NOT NULL,
  `is_umrah_seat` tinyint(1) NOT NULL,
  `trip_type` varchar(50) NOT NULL,
  `departure_stay_type` varchar(50) NOT NULL,
  `return_stay_type` varchar(50) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `booking_id` bigint(20) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingticketdetails`
--

INSERT INTO `booking_bookingticketdetails` (`id`, `is_meal_included`, `is_refundable`, `pnr`, `child_price`, `infant_price`, `adult_price`, `seats`, `weight`, `pieces`, `is_umrah_seat`, `trip_type`, `departure_stay_type`, `return_stay_type`, `status`, `booking_id`, `ticket_id`) VALUES
(1, 0, 0, '12', 1000, 1000, 10000, 14, 40, 2, 1, 'UMRAH', '1-Stop', '1-Stop', 'CONFIRMED', 11, 8),
(2, 0, 0, '12', 10000, 10000, 20000, 0, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 'Confirmed', 17, 8),
(3, 0, 1, 'Hy', 0, 0, 0, 0, 30, 2, 0, 'One-way', 'Non-Stop', 'Non-Stop', 'Confirmed', 18, 5),
(4, 0, 1, 'Hy', 0, 0, 0, 0, 30, 2, 0, 'One-way', 'Non-Stop', 'Non-Stop', 'Confirmed', 19, 5),
(5, 0, 0, '12', 100000, 80000, 120000, 0, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 'Confirmed', 20, 8),
(6, 0, 0, '12', 100000, 80000, 120000, 0, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 'Confirmed', 21, 8),
(7, 0, 0, '12', 100000, 80000, 120000, 0, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 'Confirmed', 40, 8),
(8, 0, 0, '12', 100000, 80000, 120000, 0, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 'Confirmed', 41, 8),
(9, 0, 0, '12', 1000, 1000, 10000, 14, 40, 2, 1, 'Round-trip', '1-Stop', '1-Stop', 'CONFIRMED', 48, 8),
(10, 0, 0, '12', 100000, 80000, 120000, 0, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 'Confirmed', 50, 8),
(11, 0, 0, '12', 100000, 80000, 120000, 0, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 'Confirmed', 51, 8);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingticketstopoverdetails`
--

CREATE TABLE `booking_bookingticketstopoverdetails` (
  `id` bigint(20) NOT NULL,
  `stopover_duration` varchar(100) NOT NULL,
  `trip_type` varchar(50) NOT NULL,
  `stopover_city_id` bigint(20) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingticketstopoverdetails`
--

INSERT INTO `booking_bookingticketstopoverdetails` (`id`, `stopover_duration`, `trip_type`, `stopover_city_id`, `ticket_id`) VALUES
(1, '120', 'Departure', 17, 2),
(2, '120', 'Return', 17, 2),
(3, '120', 'Return', 17, 5),
(4, '120', 'Departure', 17, 5),
(5, '120', 'Return', 17, 6),
(6, '120', 'Departure', 17, 6),
(7, '120', 'Return', 17, 7),
(8, '120', 'Departure', 17, 7),
(9, '120', 'Return', 17, 8),
(10, '120', 'Departure', 17, 8),
(11, '120', 'Return', 17, 10),
(12, '120', 'Departure', 17, 10),
(13, '120', 'Return', 17, 11),
(14, '120', 'Departure', 17, 11);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingtickettickettripdetails`
--

CREATE TABLE `booking_bookingtickettickettripdetails` (
  `id` bigint(20) NOT NULL,
  `departure_date_time` datetime(6) NOT NULL,
  `arrival_date_time` datetime(6) NOT NULL,
  `trip_type` varchar(50) NOT NULL,
  `arrival_city_id` bigint(20) NOT NULL,
  `departure_city_id` bigint(20) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingtickettickettripdetails`
--

INSERT INTO `booking_bookingtickettickettripdetails` (`id`, `departure_date_time`, `arrival_date_time`, `trip_type`, `arrival_city_id`, `departure_city_id`, `ticket_id`) VALUES
(1, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Depearture', 18, 20, 1),
(2, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 1),
(3, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Return', 18, 20, 2),
(4, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Departure', 16, 18, 2),
(5, '2025-07-09 08:53:00.000000', '2025-07-08 08:53:00.000000', 'Departure', 17, 18, 3),
(6, '2025-07-09 08:53:00.000000', '2025-07-08 08:53:00.000000', 'Departure', 17, 18, 4),
(7, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 5),
(8, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Departure', 18, 20, 5),
(9, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 6),
(10, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Departure', 18, 20, 6),
(11, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 7),
(12, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Departure', 18, 20, 7),
(13, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 8),
(14, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Departure', 18, 20, 8),
(15, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Depearture', 16, 18, 9),
(16, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Return', 18, 20, 9),
(17, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 10),
(18, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Departure', 18, 20, 10),
(19, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 11),
(20, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Departure', 18, 20, 11);

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingtransportdetails`
--

CREATE TABLE `booking_bookingtransportdetails` (
  `id` bigint(20) NOT NULL,
  `price` double NOT NULL,
  `total_price` double NOT NULL,
  `booking_id` bigint(20) NOT NULL,
  `is_price_pkr` tinyint(1) NOT NULL,
  `riyal_rate` double NOT NULL,
  `shirka_id` bigint(20) DEFAULT NULL,
  `vehicle_type_id` bigint(20) DEFAULT NULL,
  `brn_no` varchar(100) DEFAULT NULL,
  `price_in_pkr` double NOT NULL,
  `price_in_sar` double NOT NULL,
  `voucher_no` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingtransportdetails`
--

INSERT INTO `booking_bookingtransportdetails` (`id`, `price`, `total_price`, `booking_id`, `is_price_pkr`, `riyal_rate`, `shirka_id`, `vehicle_type_id`, `brn_no`, `price_in_pkr`, `price_in_sar`, `voucher_no`) VALUES
(1, 50, 50, 11, 1, 80, NULL, NULL, NULL, 0, 0, NULL),
(2, 50, 50, 48, 0, 80, NULL, NULL, NULL, 0, 0, NULL),
(3, 0, 0, 52, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(4, 0, 0, 53, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(5, 0, 0, 54, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(6, 0, 0, 55, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(7, 0, 0, 56, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(8, 0, 0, 70, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(9, 0, 0, 74, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(10, 0, 0, 75, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(11, 0, 0, 76, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(12, 0, 0, 77, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(13, 0, 0, 78, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(14, 0, 0, 79, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(15, 0, 0, 80, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(16, 0, 0, 81, 1, 0, NULL, NULL, NULL, 0, 0, NULL),
(17, 0, 0, 82, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(18, 0, 0, 85, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(19, 0, 0, 86, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(20, 0, 0, 87, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(21, 0, 0, 88, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(22, 0, 0, 89, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(23, 0, 0, 90, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(24, 0, 0, 91, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(25, 0, 0, 92, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(26, 0, 0, 93, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(27, 0, 0, 94, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(28, 0, 0, 95, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(29, 0, 0, 99, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(30, 0, 0, 100, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(31, 0, 0, 101, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(32, 0, 0, 102, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(33, 0, 0, 103, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(34, 0, 0, 105, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(35, 5000, 0, 106, 1, 0, NULL, 1, NULL, 0, 0, NULL),
(36, 5000, 0, 108, 1, 0, NULL, 1, 'BRN-MAIN-456', 5000, 0, 'VCH-MAIN-123'),
(37, 5000, 0, 110, 0, 0, NULL, 1, 'BRN-MAIN-456', 325000, 5000, 'VCH-MAIN-123'),
(38, 5000, 0, 111, 0, 65, NULL, 1, 'BRN-MAIN-456', 325000, 5000, 'VCH-MAIN-123'),
(39, 5000, 0, 112, 0, 65, NULL, 1, 'BRN-MAIN-456', 325000, 5000, 'VCH-MAIN-123');

-- --------------------------------------------------------

--
-- Table structure for table `booking_bookingtransportsector`
--

CREATE TABLE `booking_bookingtransportsector` (
  `id` bigint(20) NOT NULL,
  `sector_no` int(11) NOT NULL,
  `small_sector_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `contact_person_name` varchar(100) DEFAULT NULL,
  `voucher_no` varchar(100) DEFAULT NULL,
  `brn_no` varchar(100) DEFAULT NULL,
  `transport_detail_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_bookingtransportsector`
--

INSERT INTO `booking_bookingtransportsector` (`id`, `sector_no`, `small_sector_id`, `date`, `contact_number`, `contact_person_name`, `voucher_no`, `brn_no`, `transport_detail_id`) VALUES
(1, 1, 2, '2025-09-20', 'dsadqweq', 'test', 'adads2131', '12312wqe', 28),
(2, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 29),
(3, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 29),
(4, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 30),
(5, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 30),
(6, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 31),
(7, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 31),
(8, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 32),
(9, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 32),
(10, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 33),
(11, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 33),
(12, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 34),
(13, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 34),
(14, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 35),
(15, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 35),
(16, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 36),
(17, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 36),
(18, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 37),
(19, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 37),
(20, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 38),
(21, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 38),
(22, 2, 1, '2025-09-13', '03001234567', 'Ali Khan', 'VCH12345', 'BRN56789', 39),
(23, 3, 2, '2025-09-14', '03111234567', 'Ahmed Raza', 'VCH67890', 'BRN98765', 39);

-- --------------------------------------------------------

--
-- Table structure for table `booking_booking_internals`
--

CREATE TABLE `booking_booking_internals` (
  `id` bigint(20) NOT NULL,
  `booking_id` bigint(20) NOT NULL,
  `internalnote_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `booking_discount`
--

CREATE TABLE `booking_discount` (
  `id` bigint(20) NOT NULL,
  `things` varchar(50) NOT NULL,
  `group_ticket_discount_amount` decimal(10,2) DEFAULT NULL,
  `umrah_package_discount_amount` decimal(10,2) DEFAULT NULL,
  `currency` varchar(10) NOT NULL,
  `room_type` varchar(50) DEFAULT NULL,
  `per_night_discount` decimal(10,2) DEFAULT NULL,
  `discounted_hotels` int(11) DEFAULT NULL,
  `discount_group_id` bigint(20) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_discount`
--

INSERT INTO `booking_discount` (`id`, `things`, `group_ticket_discount_amount`, `umrah_package_discount_amount`, `currency`, `room_type`, `per_night_discount`, `discounted_hotels`, `discount_group_id`, `organization_id`) VALUES
(1, 'group_ticket', 1000.00, NULL, 'PKR', NULL, NULL, NULL, 1, 8),
(2, 'umrah_package', NULL, 5000.00, 'SAR', NULL, NULL, NULL, 1, 8),
(3, 'hotel', NULL, NULL, 'PKR', 'double', 200.00, NULL, 1, 8),
(4, 'group_ticket', 1000.00, NULL, 'PKR', NULL, NULL, NULL, 2, 8),
(5, 'umrah_package', NULL, 5000.00, 'SAR', NULL, NULL, NULL, 2, 8),
(6, 'hotel', NULL, NULL, 'PKR', 'double', 200.00, NULL, 2, 8);

-- --------------------------------------------------------

--
-- Table structure for table `booking_discountgroup`
--

CREATE TABLE `booking_discountgroup` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_discountgroup`
--

INSERT INTO `booking_discountgroup` (`id`, `name`, `is_active`, `organization_id`) VALUES
(1, 'Ramzan Special', 1, 8),
(2, 'Ramzan Special', 1, 8);

-- --------------------------------------------------------

--
-- Table structure for table `booking_internalnote`
--

CREATE TABLE `booking_internalnote` (
  `id` bigint(20) NOT NULL,
  `note_type` varchar(255) NOT NULL,
  `follow_up_date` date DEFAULT NULL,
  `date_time` datetime(6) NOT NULL,
  `note` longtext NOT NULL,
  `attachment` varchar(100) DEFAULT NULL,
  `working_status` varchar(20) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `booking_markup`
--

CREATE TABLE `booking_markup` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `applies_to` varchar(20) NOT NULL,
  `ticket_markup` double DEFAULT NULL,
  `hotel_per_night_markup` double DEFAULT NULL,
  `umrah_package_markup` double DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_markup`
--

INSERT INTO `booking_markup` (`id`, `name`, `applies_to`, `ticket_markup`, `hotel_per_night_markup`, `umrah_package_markup`, `organization_id`, `created_at`, `updated_at`) VALUES
(1, 'Summer Ticket Markup', 'group_ticket', 1500, 0, 0, 8, '2025-09-29 11:23:10.789728', '2025-09-29 11:23:10.789840');

-- --------------------------------------------------------

--
-- Table structure for table `booking_organizationlink`
--

CREATE TABLE `booking_organizationlink` (
  `id` bigint(20) NOT NULL,
  `organization_id` int(11) NOT NULL,
  `this_organization_request` varchar(20) NOT NULL,
  `main_organization_request` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `request_status` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `booking_organizationlink`
--

INSERT INTO `booking_organizationlink` (`id`, `organization_id`, `this_organization_request`, `main_organization_request`, `created_at`, `updated_at`, `request_status`) VALUES
(1, 5, 'ACCEPTED', 'REJECTED', '2025-09-27 15:30:23.613252', '2025-09-27 15:35:35.000345', 'PENDING'),
(2, 6, 'REJECTED', 'ACCEPTED', '2025-09-27 15:30:23.617502', '2025-09-27 15:30:23.617554', 'PENDING'),
(3, 5, 'PENDING', 'ACCEPTED', '2025-09-27 15:31:56.791730', '2025-09-27 15:31:56.791832', 'PENDING'),
(4, 6, 'REJECTED', 'ACCEPTED', '2025-09-27 15:31:56.793813', '2025-09-27 15:31:56.793847', 'PENDING');

-- --------------------------------------------------------

--
-- Table structure for table `booking_payment`
--

CREATE TABLE `booking_payment` (
  `id` bigint(20) NOT NULL,
  `method` varchar(50) NOT NULL,
  `amount` double NOT NULL,
  `date` datetime(6) NOT NULL,
  `remarks` longtext DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `agency_id` bigint(20) DEFAULT NULL,
  `agent_id` int(11) DEFAULT NULL,
  `bank_id` bigint(20) DEFAULT NULL,
  `booking_id` bigint(20) DEFAULT NULL,
  `branch_id` bigint(20) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `organization_id` bigint(20) NOT NULL,
  `transaction_number` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'users', 'userprofile'),
(8, 'users', 'permissionextension'),
(9, 'users', 'groupextension'),
(10, 'organization', 'organization'),
(11, 'organization', 'branch'),
(12, 'users', 'userfiles'),
(13, 'packages', 'airlines'),
(14, 'packages', 'city'),
(15, 'packages', 'shirka'),
(16, 'packages', 'transportsectorprice'),
(17, 'packages', 'umrahvisaprice'),
(18, 'packages', 'bookingexpiry'),
(19, 'packages', 'riyalrate'),
(20, 'tickets', 'tickerstopoverdetails'),
(21, 'tickets', 'hotelprices'),
(22, 'tickets', 'tickettripdetails'),
(23, 'tickets', 'ticket'),
(24, 'tickets', 'hotels'),
(25, 'packages', 'umrahpackage'),
(26, 'packages', 'umrahpackagetransportdetails'),
(27, 'packages', 'umrahpackageticketdetails'),
(28, 'packages', 'umrahpackagehoteldetails'),
(29, 'organization', 'agency'),
(30, 'packages', 'umrahpackagediscountdetails'),
(31, 'packages', 'customumrahpackage'),
(32, 'packages', 'umrahvisapricetwo'),
(33, 'packages', 'umrahvisapricetwohotel'),
(34, 'packages', 'customumrahpackagetransportdetails'),
(35, 'packages', 'customumrahpackageticketdetails'),
(36, 'packages', 'customumrahpackagehoteldetails'),
(37, 'packages', 'onlyvisaprice'),
(38, 'booking', 'booking'),
(39, 'booking', 'bookingdetail'),
(40, 'organization', 'agencyfiles'),
(41, 'organization', 'agencycontact'),
(42, 'packages', 'setvisatype'),
(43, 'packages', 'ziaratprice'),
(44, 'packages', 'foodprice'),
(45, 'tickets', 'hotelcontactdetails'),
(46, 'tickets', 'hotelrooms'),
(47, 'tickets', 'roomdetails'),
(48, 'packages', 'customumrahfooddetails'),
(49, 'packages', 'customumrahziaratdetails'),
(50, 'booking', 'bank'),
(51, 'booking', 'bookinghoteldetails'),
(52, 'booking', 'bookingpersondetail'),
(53, 'booking', 'bookingticketdetails'),
(54, 'booking', 'bookingticketstopoverdetails'),
(55, 'booking', 'bookingtickettickettripdetails'),
(56, 'booking', 'bookingtransportdetails'),
(57, 'booking', 'payment'),
(58, 'booking', 'bookingpersonziyaratdetails'),
(59, 'booking', 'bookingpersonfooddetails'),
(60, 'booking', 'bookingpersoncontactdetails'),
(61, 'booking', 'sector'),
(62, 'booking', 'bigsector'),
(63, 'booking', 'vehicletype'),
(64, 'booking', 'internalnote'),
(65, 'booking', 'bookingtransportsector'),
(66, 'booking', 'bankaccount'),
(67, 'booking', 'organizationlink'),
(68, 'booking', 'allowedreseller'),
(69, 'booking', 'discount'),
(70, 'booking', 'discountgroup'),
(71, 'booking', 'markup');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-25 20:34:22.157548'),
(2, 'auth', '0001_initial', '2025-06-25 20:34:23.290901'),
(3, 'admin', '0001_initial', '2025-06-25 20:34:23.643187'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-06-25 20:34:23.657006'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-25 20:34:23.671646'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-06-25 20:34:23.804617'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-06-25 20:34:23.863153'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-06-25 20:34:23.910661'),
(9, 'auth', '0004_alter_user_username_opts', '2025-06-25 20:34:23.926957'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-06-25 20:34:23.996814'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-06-25 20:34:24.000433'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-06-25 20:34:24.022354'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-06-25 20:34:24.123826'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-06-25 20:34:24.187784'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-06-25 20:34:24.283779'),
(16, 'auth', '0011_update_proxy_permissions', '2025-06-25 20:34:24.332312'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-06-25 20:34:24.383350'),
(18, 'organization', '0001_initial', '2025-06-25 20:34:25.393264'),
(19, 'sessions', '0001_initial', '2025-06-25 20:34:25.492058'),
(20, 'users', '0001_initial', '2025-06-25 20:34:25.838502'),
(21, 'users', '0002_userfiles', '2025-06-28 08:10:16.510859'),
(22, 'packages', '0001_initial', '2025-07-03 21:46:56.957247'),
(23, 'tickets', '0001_initial', '2025-07-03 21:46:57.771863'),
(24, 'tickets', '0002_alter_hotels_city', '2025-07-09 22:24:13.763785'),
(25, 'packages', '0002_riyalrate_is_hotel_pkr_riyalrate_is_transport_pkr_and_more', '2025-07-09 22:24:13.952594'),
(26, 'packages', '0003_umrahpackage_umrahpackagetransportdetails_and_more', '2025-07-09 22:24:14.522590'),
(27, 'organization', '0002_agency', '2025-07-15 21:21:47.072806'),
(28, 'packages', '0004_remove_umrahpackage_discount_max_adault_age_and_more', '2025-07-15 21:21:51.778825'),
(29, 'packages', '0005_umrahvisapricetwo_and_more', '2025-07-15 21:21:54.361277'),
(30, 'packages', '0006_transportsectorprice_only_transport_charge_and_more', '2025-07-15 21:21:54.688937'),
(31, 'booking', '0001_initial', '2025-07-15 21:23:01.254868'),
(32, 'organization', '0003_remove_agency_logo_agency_address_agency_ageny_name_and_more', '2025-07-16 20:05:28.801525'),
(33, 'organization', '0004_agencycontact', '2025-07-16 20:05:28.913250'),
(34, 'packages', '0007_remove_customumrahpackage_visa_price_and_more', '2025-07-16 20:05:30.124410'),
(35, 'tickets', '0003_hotels_status_ticket_status', '2025-07-16 20:05:30.225925'),
(36, 'users', '0003_remove_userprofile_address_and_more', '2025-07-16 20:05:30.363155'),
(37, 'organization', '0005_agency_logo', '2025-07-21 17:25:32.123194'),
(38, 'packages', '0008_remove_umrahpackage_visa_price_and_more', '2025-07-21 17:25:32.469255'),
(39, 'tickets', '0004_remove_ticket_price_ticket_adult_price_and_more', '2025-07-21 17:25:32.894790'),
(40, 'packages', '0009_customumrahpackage_created_at_and_more', '2025-07-24 19:53:22.506822'),
(41, 'packages', '0010_riyalrate_is_food_pkr_riyalrate_is_ziarat_pkr_and_more', '2025-07-30 20:02:40.538524'),
(42, 'tickets', '0005_hotelcontactdetails', '2025-07-30 20:02:40.676614'),
(43, 'tickets', '0006_hotelrooms_roomdetails', '2025-07-30 20:02:40.968926'),
(44, 'packages', '0011_customumrahpackagehoteldetails_quantity', '2025-07-31 16:45:58.006416'),
(45, 'tickets', '0007_remove_hotelprices_double_price_and_more', '2025-07-31 16:45:58.390691'),
(46, 'packages', '0012_customumrahziaratdetails_customumrahfooddetails', '2025-07-31 17:06:55.351970'),
(47, 'booking', '0002_bank_bookinghoteldetails_bookingpersondetail_and_more', '2025-08-15 13:52:28.904859'),
(48, 'packages', '0013_alter_onlyvisaprice_airpot_name', '2025-08-19 10:02:42.661017'),
(49, 'booking', '0003_rename_madinah_ziyarat_price_bookingpersondetail_ziyarat_price_and_more', '2025-08-19 10:02:46.150860'),
(50, 'booking', '0004_remove_bookingpersondetail_voucher_number_and_more', '2025-08-19 10:02:47.711591'),
(51, 'booking', '0005_remove_bookingpersondetail_food_price_and_more', '2025-08-23 00:01:25.849303'),
(52, 'tickets', '0008_rename_seats_ticket_total_seats_and_more', '2025-08-23 00:01:26.261783'),
(53, 'packages', '0014_rename_name_ziaratprice_ziarat_title_and_more', '2025-09-14 13:21:44.477308'),
(54, 'packages', '0015_foodprice_city_foodprice_description_foodprice_price', '2025-09-14 13:40:27.040244'),
(55, 'booking', '0006_sector', '2025-09-15 14:29:19.862615'),
(56, 'booking', '0007_alter_sector_organization_alter_sector_table', '2025-09-15 15:16:03.254412'),
(57, 'booking', '0008_alter_sector_organization_alter_sector_table_and_more', '2025-09-15 15:16:03.739306'),
(58, 'booking', '0009_vehicletype', '2025-09-15 16:12:24.413834'),
(59, 'booking', '0010_rename_check_in_time_bookinghoteldetails_check_in_date_and_more', '2025-09-15 16:39:37.213261'),
(60, 'booking', '0011_bookinghoteldetails_contact_person_name_and_more', '2025-09-15 18:09:19.356705'),
(61, 'booking', '0012_remove_sector_sector_name_sector_arrival_city_and_more', '2025-09-17 11:02:01.185759'),
(62, 'packages', '0016_ziaratprice_max_pex_ziaratprice_min_pex_and_more', '2025-09-17 11:16:21.690174'),
(63, 'booking', '0013_remove_bookingtransportdetails_vehicle_type', '2025-09-17 11:26:32.926311'),
(64, 'booking', '0014_bookingtransportdetails_vehicle_type', '2025-09-17 11:30:36.743459'),
(65, 'booking', '0015_remove_bookingtransportdetails_transport_sector', '2025-09-17 11:34:34.731816'),
(66, 'booking', '0016_remove_bookingpersondetail_food_brn_and_more', '2025-09-17 16:55:09.210990'),
(67, 'booking', '0017_bookingpersondetail_food_brn_and_more', '2025-09-17 16:57:21.236614'),
(68, 'booking', '0018_remove_bookingticketdetails_is_price_pkr_and_more', '2025-09-17 17:32:39.802770'),
(69, 'booking', '0019_remove_bookingpersondetail_food_brn_and_more', '2025-09-17 17:46:29.957683'),
(70, 'booking', '0020_remove_bigsector_contact_name_and_more', '2025-09-18 11:33:36.126816'),
(71, 'booking', '0021_alter_bigsector_organization_alter_bigsector_table', '2025-09-18 11:41:50.107991'),
(72, 'booking', '0022_rename_type_vehicletype_visa_type', '2025-09-18 11:46:30.383249'),
(73, 'packages', '0017_onlyvisaprice_city_onlyvisaprice_status', '2025-09-18 11:55:03.036100'),
(74, 'booking', '0023_bookinghoteldetails_check_in_status_and_more', '2025-09-18 12:07:02.579698'),
(75, 'packages', '0018_umrahvisapricetwo_vehicle_type', '2025-09-18 19:20:54.167698'),
(76, 'booking', '0024_booking_created_at', '2025-09-18 19:29:39.681153'),
(77, 'booking', '0025_booking_action_booking_notes_booking_rejected_at', '2025-09-18 19:34:09.791480'),
(78, 'booking', '0026_bookinghoteldetails_hotel_brn_and_more', '2025-09-19 09:51:00.398612'),
(79, 'booking', '0027_booking_call_status_booking_client_note_and_more', '2025-09-19 10:22:50.520873'),
(80, 'booking', '0028_internalnote', '2025-09-19 10:55:17.099274'),
(81, 'tickets', '0009_alter_hotels_city', '2025-09-19 11:04:54.931632'),
(82, 'packages', '0019_rename_check_in_time_umrahpackagehoteldetails_check_in_date_and_more', '2025-09-19 11:16:39.092874'),
(83, 'booking', '0029_bookingpersondetail_contact_number_and_more', '2025-09-19 11:36:40.126834'),
(84, 'booking', '0030_bookingtransportsector', '2025-09-20 14:22:05.032838'),
(85, 'booking', '0031_alter_bookingtransportsector_transport_detail', '2025-09-20 14:40:55.918124'),
(86, 'booking', '0032_bookingtransportdetails_brn_no_and_more', '2025-09-20 14:48:59.509862'),
(87, 'booking', '0033_booking_is_visa_price_pkr_booking_visa_rate_and_more', '2025-09-20 15:11:23.046828'),
(88, 'booking', '0034_bookinghoteldetails_self_hotel_name_and_more', '2025-09-20 17:10:37.885066'),
(89, 'booking', '0035_remove_bookingpersondetail_is_food_included_and_more', '2025-09-20 17:16:16.741535'),
(90, 'booking', '0036_booking_internal', '2025-09-20 17:41:38.729347'),
(91, 'booking', '0037_internalnote_created_at', '2025-09-20 17:47:25.684439'),
(92, 'booking', '0038_booking_rejected_employer', '2025-09-20 17:50:33.124260'),
(93, 'packages', '0020_umrahpackage_booked_seats_and_more', '2025-09-20 17:58:52.859580'),
(94, 'booking', '0039_bookingpersonziyaratdetails_contact_number_and_more', '2025-09-20 19:04:31.366442'),
(95, 'booking', '0040_bookingpersonfooddetails_contact_number_and_more', '2025-09-20 19:07:40.809666'),
(96, 'booking', '0041_bookingpersondetail_is_visa_price_pkr_and_more', '2025-09-20 19:10:35.649228'),
(97, 'booking', '0042_remove_booking_internal_booking_internals', '2025-09-20 19:14:05.553376'),
(98, 'booking', '0043_alter_bookingpersondetail_ticket_discount_and_more', '2025-09-21 13:53:01.577120'),
(99, 'booking', '0044_alter_bookingpersondetail_ticket_discount_and_more', '2025-09-21 13:53:01.808139'),
(100, 'packages', '0021_rename_check_in_time_customumrahpackagehoteldetails_check_in_date_and_more', '2025-09-21 13:53:04.609126'),
(101, 'packages', '0022_alter_umrahpackagetransportdetails_vehicle_type', '2025-09-21 13:54:51.327190'),
(102, 'packages', '0023_remove_customumrahpackagetransportdetails_transport_sector_and_more', '2025-09-21 13:57:10.796318'),
(103, 'booking', '0045_rename_notes_booking_rejected_notes', '2025-09-21 14:11:30.374126'),
(104, 'packages', '0024_remove_customumrahpackage_agent', '2025-09-21 14:11:31.077658'),
(105, 'packages', '0025_airlines_is_umrah_seat', '2025-09-21 14:23:31.479551'),
(106, 'packages', '0026_remove_umrahvisapricetwo_vehicle_type_and_more', '2025-09-21 19:11:14.711510'),
(107, 'booking', '0046_booking_confirmed_by', '2025-09-23 12:00:17.354851'),
(108, 'packages', '0027_customumrahpackage_user', '2025-09-23 12:08:46.345742'),
(109, 'booking', '0047_bankaccount', '2025-09-23 12:16:49.029506'),
(110, 'booking', '0048_booking_owner_organization_id_and_more', '2025-09-25 11:17:48.950947'),
(111, 'booking', '0049_alter_bankaccount_agency_alter_bankaccount_branch_and_more', '2025-09-25 11:21:17.444034'),
(112, 'booking', '0050_organizationlink', '2025-09-27 15:26:12.125070'),
(113, 'booking', '0051_booking_booking_organization_id_and_more', '2025-09-27 15:39:30.334328'),
(114, 'tickets', '0010_ticket_inventory_owner_organization_id', '2025-09-27 15:45:45.546418'),
(115, 'packages', '0028_umrahpackage_inventory_owner_organization_id', '2025-09-27 15:49:38.012148'),
(116, 'booking', '0052_allowedreseller', '2025-09-27 15:53:35.943464'),
(117, 'booking', '0053_alter_allowedreseller_inventory_owner_company', '2025-09-27 16:00:26.496867'),
(118, 'booking', '0054_organizationlink_request_status', '2025-09-29 10:43:45.745087'),
(119, 'booking', '0055_discountgroup_discount', '2025-09-29 10:55:11.984543'),
(120, 'booking', '0056_markup', '2025-09-29 11:18:02.293682'),
(121, 'booking', '0057_alter_markup_organization_id', '2025-09-29 11:25:22.805863'),
(122, 'booking', '0058_alter_bank_account_title_alter_bank_name_and_more', '2025-09-29 11:32:41.328613'),
(123, 'packages', '0029_umrahpackagetransportdetails_transport_type', '2025-09-29 18:09:40.944301');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('pcipk1kkkcvf0zy5of7hc8yhn9l0gn8b', '.eJxVjMsOwiAQRf-FtSEM77p07zeQAQapGkhKuzL-uzbpQrf3nHNfLOC21rANWsKc2ZkBO_1uEdOD2g7yHdut89TbusyR7wo_6ODXnul5Ody_g4qjfmudnSzeFDBGTlZnsAISCAAvbVZWOmkwejdZoQl0SUoikUUwJTpS2rP3B6fxNq4:1uXPyB:dqCjlZduCDQtneWyX81G-mC0SYCDqCH_6SAIEJHny-w', '2025-07-17 19:51:43.820261');

-- --------------------------------------------------------

--
-- Table structure for table `organization_agency`
--

CREATE TABLE `organization_agency` (
  `id` bigint(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `branch_id` bigint(20) NOT NULL,
  `address` longtext DEFAULT NULL,
  `ageny_name` varchar(30) DEFAULT NULL,
  `agreement_status` tinyint(1) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `organization_agency`
--

INSERT INTO `organization_agency` (`id`, `name`, `branch_id`, `address`, `ageny_name`, `agreement_status`, `email`, `phone_number`, `logo`) VALUES
(10, 'Ahsan Raza', 19, 'Ali pur chatthas', 'Saer.pk', 1, 'ahsaan.raza.butt@gmail.com', '03000709017', 'media/agency_logos/ali.png'),
(6, 'Ali', 14, 'malik market Lahore', 'Ali Travels', 1, 'ahsan@gmail.com', '1234567890', ''),
(11, 'Saer', 19, 'Ali Pur Chattha Near bus stand', 'Ahsan raza', 1, 'ahsaan.raza.butt@gmail.com', '+923000709017', ''),
(12, 'MIR', 14, '767897', 'MIR TRAVEL', 1, 'MIR@GMAIL.COM', '892067`', '');

-- --------------------------------------------------------

--
-- Table structure for table `organization_agencycontact`
--

CREATE TABLE `organization_agencycontact` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `remarks` varchar(50) DEFAULT NULL,
  `agency_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `organization_agencyfiles`
--

CREATE TABLE `organization_agencyfiles` (
  `id` bigint(20) NOT NULL,
  `file` varchar(100) NOT NULL,
  `file_type` varchar(50) DEFAULT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `description` longtext DEFAULT NULL,
  `agency_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `organization_agency_user`
--

CREATE TABLE `organization_agency_user` (
  `id` bigint(20) NOT NULL,
  `agency_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `organization_agency_user`
--

INSERT INTO `organization_agency_user` (`id`, `agency_id`, `user_id`) VALUES
(21, 10, 32),
(9, 10, 20),
(10, 10, 24),
(18, 10, 29),
(19, 10, 30);

-- --------------------------------------------------------

--
-- Table structure for table `organization_branch`
--

CREATE TABLE `organization_branch` (
  `id` bigint(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `organization_branch`
--

INSERT INTO `organization_branch` (`id`, `name`, `contact_number`, `email`, `address`, `organization_id`) VALUES
(19, 'new', '1234567890', 'new@gmail.com', '1234567890', 8),
(13, 'Saer-saepk', '+923000709017', 'ahsaan.raza.butt@gmail.com', 'Ali Pur Chattha Near bus stand\nGujrawala Road', 5),
(14, 'Saer-HBL', '+923000709017', 'ahsaan.raza.butt@gmail.com', 'Ali Pur Chattha Near bus stand\nGujrawala Roads', 8),
(15, 'malik store', '12356789076532', 'info@codedthemes.com', '1234567890', 5),
(18, 'zain shahzad', '222', 'ahsaan.razabutt@gmail.com', 'Alipur Chatha, village wazir ke chattha', 7);

-- --------------------------------------------------------

--
-- Table structure for table `organization_branch_user`
--

CREATE TABLE `organization_branch_user` (
  `id` bigint(20) NOT NULL,
  `branch_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `organization_branch_user`
--

INSERT INTO `organization_branch_user` (`id`, `branch_id`, `user_id`) VALUES
(24, 14, 21),
(28, 14, 29),
(23, 14, 20),
(33, 19, 34),
(32, 14, 33),
(29, 19, 30),
(31, 14, 32);

-- --------------------------------------------------------

--
-- Table structure for table `organization_organization`
--

CREATE TABLE `organization_organization` (
  `id` bigint(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `organization_organization`
--

INSERT INTO `organization_organization` (`id`, `name`, `phone_number`, `email`, `address`, `logo`) VALUES
(8, 'HBL', '1234567890', 'hbl@gmail.com', 'qwertyuio', 'media/organization_logos/jonatan-pie-h8nxGssjQXs-unsplash_8AcYCHw.jpg'),
(7, 'alfa.pk', '03000709017', 'ahsaan.raza.butt@gmail.com', 'Ali Pur Chattha Near bus stand\r\nGujrawala Road', 'media/organization_logos/FACEBOOK_COVER_vpNDied.png'),
(5, 'saer.pk', '+923000709017', 'ahsaan.raza.butt@gmail.com', 'Ali Pur Chattha Near bus stand\r\nGujrawala Roads', 'media/organization_logos/logo.png');

-- --------------------------------------------------------

--
-- Table structure for table `organization_organization_user`
--

CREATE TABLE `organization_organization_user` (
  `id` bigint(20) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `organization_organization_user`
--

INSERT INTO `organization_organization_user` (`id`, `organization_id`, `user_id`) VALUES
(36, 8, 33),
(32, 8, 29),
(27, 7, 20),
(37, 8, 34),
(28, 7, 21),
(33, 8, 30),
(35, 7, 32);

-- --------------------------------------------------------

--
-- Table structure for table `packages_airlines`
--

CREATE TABLE `packages_airlines` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `organization_id` bigint(20) NOT NULL,
  `is_umrah_seat` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_airlines`
--

INSERT INTO `packages_airlines` (`id`, `name`, `code`, `logo`, `organization_id`, `is_umrah_seat`) VALUES
(17, 'saudia', 'sv', 'media/airlines_logos/Frame_1171276509.png', 7, 1),
(16, 'Saudi', 'Sv', 'media/airlines_logos/c9df85e0-3ada-4ca4-bb00-73f82e62245f.jpeg', 7, 1),
(14, 'Pakistan international airline', 'PIA', 'media/airlines_logos/Pakistan-International-Airlines-Logo.png', 8, 1),
(15, 'Saudi airline', 'SV', 'media/airlines_logos/saudia-airlines-logo-png_seeklogo-268083.png', 8, 1);

-- --------------------------------------------------------

--
-- Table structure for table `packages_bookingexpiry`
--

CREATE TABLE `packages_bookingexpiry` (
  `id` bigint(20) NOT NULL,
  `umrah_expiry_time` int(11) NOT NULL,
  `ticket_expiry_time` int(11) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_bookingexpiry`
--

INSERT INTO `packages_bookingexpiry` (`id`, `umrah_expiry_time`, `ticket_expiry_time`, `organization_id`) VALUES
(1, 109, 10, 8),
(2, 10, 10, 8);

-- --------------------------------------------------------

--
-- Table structure for table `packages_city`
--

CREATE TABLE `packages_city` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_city`
--

INSERT INTO `packages_city` (`id`, `name`, `code`, `organization_id`) VALUES
(5, 'Karachi', 'Khi', 7),
(6, 'Lahore', 'Lhe', 7),
(7, 'Dubai', 'Dxb', 7),
(8, 'Jeddah', 'Jed', 7),
(20, 'Madina', 'Med', 8),
(19, 'Makkah', 'mak', 8),
(18, 'Karachi', 'Khi', 8),
(17, 'Dubai', 'Dxb', 8),
(16, 'Jeddah', 'Jed', 8),
(15, 'LAHORE', 'Lhe', 8),
(21, 'Sialkot', 'SKT', 8);

-- --------------------------------------------------------

--
-- Table structure for table `packages_customumrahfooddetails`
--

CREATE TABLE `packages_customumrahfooddetails` (
  `id` bigint(20) NOT NULL,
  `food_id` bigint(20) NOT NULL,
  `package_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_customumrahfooddetails`
--

INSERT INTO `packages_customumrahfooddetails` (`id`, `food_id`, `package_id`) VALUES
(1, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `packages_customumrahpackage`
--

CREATE TABLE `packages_customumrahpackage` (
  `id` bigint(20) NOT NULL,
  `total_adaults` int(11) NOT NULL,
  `total_children` int(11) NOT NULL,
  `total_infants` int(11) NOT NULL,
  `long_term_stay` tinyint(1) NOT NULL,
  `is_full_transport` tinyint(1) NOT NULL,
  `is_one_side_transport` tinyint(1) NOT NULL,
  `only_visa` tinyint(1) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `adault_visa_price` double NOT NULL,
  `agency_id` bigint(20) NOT NULL,
  `child_visa_price` double NOT NULL,
  `infant_visa_price` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_customumrahpackage`
--

INSERT INTO `packages_customumrahpackage` (`id`, `total_adaults`, `total_children`, `total_infants`, `long_term_stay`, `is_full_transport`, `is_one_side_transport`, `only_visa`, `organization_id`, `adault_visa_price`, `agency_id`, `child_visa_price`, `infant_visa_price`, `created_at`, `status`, `updated_at`, `user_id`) VALUES
(14, 1, 1, 1, 1, 1, 1, 1, 8, 45.09, 10, 90.88, 889.08, '2025-09-14 17:25:34.000000', 'Pending', '2025-09-14 17:25:34.000000', 33);

-- --------------------------------------------------------

--
-- Table structure for table `packages_customumrahpackagehoteldetails`
--

CREATE TABLE `packages_customumrahpackagehoteldetails` (
  `id` bigint(20) NOT NULL,
  `room_type` varchar(20) DEFAULT NULL,
  `sharing_type` varchar(20) DEFAULT NULL,
  `check_in_date` date DEFAULT NULL,
  `check_out_date` date DEFAULT NULL,
  `number_of_nights` int(11) NOT NULL,
  `special_request` longtext DEFAULT NULL,
  `price` double NOT NULL,
  `hotel_id` bigint(20) NOT NULL,
  `package_id` bigint(20) NOT NULL,
  `quantity` double NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_customumrahpackagehoteldetails`
--

INSERT INTO `packages_customumrahpackagehoteldetails` (`id`, `room_type`, `sharing_type`, `check_in_date`, `check_out_date`, `number_of_nights`, `special_request`, `price`, `hotel_id`, `package_id`, `quantity`) VALUES
(1, 'Quint Bed', 'Family Only', '2025-08-11', '2025-08-31', 20, 'Thanks', 10500, 16, 1, 15),
(3, 'Double Bed', 'Male Only', '2025-08-12', '2025-08-30', 18, 'Malik', 10500, 16, 3, 3),
(4, 'Double Bed', 'Male Only', '2025-08-12', '2025-08-30', 18, 'Malik', 10500, 16, 4, 3);

-- --------------------------------------------------------

--
-- Table structure for table `packages_customumrahpackageticketdetails`
--

CREATE TABLE `packages_customumrahpackageticketdetails` (
  `id` bigint(20) NOT NULL,
  `package_id` bigint(20) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_customumrahpackageticketdetails`
--

INSERT INTO `packages_customumrahpackageticketdetails` (`id`, `package_id`, `ticket_id`) VALUES
(1, 1, 20),
(3, 3, 21),
(4, 4, 21);

-- --------------------------------------------------------

--
-- Table structure for table `packages_customumrahpackagetransportdetails`
--

CREATE TABLE `packages_customumrahpackagetransportdetails` (
  `id` bigint(20) NOT NULL,
  `vehicle_type` int(11) DEFAULT NULL,
  `package_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_customumrahpackagetransportdetails`
--

INSERT INTO `packages_customumrahpackagetransportdetails` (`id`, `vehicle_type`, `package_id`) VALUES
(1, 0, 1),
(3, 0, 3),
(4, 0, 4);

-- --------------------------------------------------------

--
-- Table structure for table `packages_customumrahziaratdetails`
--

CREATE TABLE `packages_customumrahziaratdetails` (
  `id` bigint(20) NOT NULL,
  `package_id` bigint(20) NOT NULL,
  `ziarat_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_customumrahziaratdetails`
--

INSERT INTO `packages_customumrahziaratdetails` (`id`, `package_id`, `ziarat_id`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `packages_foodprice`
--

CREATE TABLE `packages_foodprice` (
  `id` bigint(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `min_pex` int(11) NOT NULL,
  `per_pex` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `city_id` bigint(20) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `price` double NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_foodprice`
--

INSERT INTO `packages_foodprice` (`id`, `title`, `min_pex`, `per_pex`, `active`, `organization_id`, `city_id`, `description`, `price`) VALUES
(3, 'Rice', 12, 100, 1, 8, 19, 'Protect your Health.', 1200),
(11, 'Wheat', 10, 10, 1, 8, 20, 'Wheat is good for health', 100);

-- --------------------------------------------------------

--
-- Table structure for table `packages_onlyvisaprice`
--

CREATE TABLE `packages_onlyvisaprice` (
  `id` bigint(20) NOT NULL,
  `adault_price` double NOT NULL,
  `child_price` double NOT NULL,
  `infant_price` double NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `airpot_name` varchar(100) DEFAULT NULL,
  `max_days` varchar(50) NOT NULL,
  `min_days` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  `city_id` bigint(20) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `packages_riyalrate`
--

CREATE TABLE `packages_riyalrate` (
  `id` bigint(20) NOT NULL,
  `rate` double NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `is_hotel_pkr` tinyint(1) NOT NULL,
  `is_transport_pkr` tinyint(1) NOT NULL,
  `is_visa_pkr` tinyint(1) NOT NULL,
  `is_food_pkr` tinyint(1) NOT NULL,
  `is_ziarat_pkr` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_riyalrate`
--

INSERT INTO `packages_riyalrate` (`id`, `rate`, `organization_id`, `is_hotel_pkr`, `is_transport_pkr`, `is_visa_pkr`, `is_food_pkr`, `is_ziarat_pkr`) VALUES
(5, 65, 8, 0, 0, 0, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `packages_setvisatype`
--

CREATE TABLE `packages_setvisatype` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_setvisatype`
--

INSERT INTO `packages_setvisatype` (`id`, `name`, `organization_id`) VALUES
(23, 'type2', 8);

-- --------------------------------------------------------

--
-- Table structure for table `packages_shirka`
--

CREATE TABLE `packages_shirka` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_shirka`
--

INSERT INTO `packages_shirka` (`id`, `name`, `organization_id`) VALUES
(13, 'ABDUL RAZZAQ AL KUTBI', 8),
(5, 'abdul Razzaq', 7),
(12, 'Abdul razzaq al kutbi', 8);

-- --------------------------------------------------------

--
-- Table structure for table `packages_transportsectorprice`
--

CREATE TABLE `packages_transportsectorprice` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `vehicle_type` int(11) DEFAULT NULL,
  `adault_price` double NOT NULL,
  `child_price` double NOT NULL,
  `infant_price` double NOT NULL,
  `is_visa` tinyint(1) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `only_transport_charge` tinyint(1) NOT NULL,
  `reference` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_transportsectorprice`
--

INSERT INTO `packages_transportsectorprice` (`id`, `name`, `vehicle_type`, `adault_price`, `child_price`, `infant_price`, `is_visa`, `organization_id`, `only_transport_charge`, `reference`) VALUES
(7, 'JED-MAK-MED-MAK-JED', 0, 50, 50, 50, 0, 8, 1, 'type2'),
(6, 'JED(A)-MAK(H)-MED(H)-MED(A)', 0, 50, 50, 51, 1, 8, 0, 'type1'),
(8, 'MED-JED-MAK-JED(A)', 0, 50, 50, 50, 0, 8, 1, 'type2'),
(9, 'JED(A)-MAK(H)', 0, 550, 200, 150, 1, 8, 0, 'type1'),
(10, 'string', 0, 5877.353181940696, 9289.767574447538, 6548.2939903459055, 1, 8, 0, 'string');

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahpackage`
--

CREATE TABLE `packages_umrahpackage` (
  `id` bigint(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `rules` longtext DEFAULT NULL,
  `total_seats` bigint(20) DEFAULT NULL,
  `food_price` double NOT NULL,
  `makkah_ziyarat_price` double NOT NULL,
  `madinah_ziyarat_price` double NOT NULL,
  `transport_price` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `adault_service_charge` double NOT NULL,
  `child_service_charge` double NOT NULL,
  `infant_service_charge` double NOT NULL,
  `filght_min_adault_age` int(11) NOT NULL,
  `filght_max_adault_age` int(11) NOT NULL,
  `max_chilld_allowed` int(11) NOT NULL,
  `max_infant_allowed` int(11) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `is_double_active` tinyint(1) NOT NULL,
  `is_quad_active` tinyint(1) NOT NULL,
  `is_quaint_active` tinyint(1) NOT NULL,
  `is_sharing_active` tinyint(1) NOT NULL,
  `is_triple_active` tinyint(1) NOT NULL,
  `adault_partial_payment` double NOT NULL,
  `child_partial_payment` double NOT NULL,
  `infant_partial_payment` double NOT NULL,
  `is_partial_payment_active` tinyint(1) NOT NULL,
  `is_service_charge_active` tinyint(1) NOT NULL,
  `adault_visa_price` double NOT NULL,
  `child_visa_price` double NOT NULL,
  `infant_visa_price` double NOT NULL,
  `booked_seats` bigint(20) DEFAULT NULL,
  `confirmed_seats` bigint(20) DEFAULT NULL,
  `left_seats` bigint(20) DEFAULT NULL,
  `inventory_owner_organization_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahpackage`
--

INSERT INTO `packages_umrahpackage` (`id`, `title`, `rules`, `total_seats`, `food_price`, `makkah_ziyarat_price`, `madinah_ziyarat_price`, `transport_price`, `is_active`, `adault_service_charge`, `child_service_charge`, `infant_service_charge`, `filght_min_adault_age`, `filght_max_adault_age`, `max_chilld_allowed`, `max_infant_allowed`, `organization_id`, `is_double_active`, `is_quad_active`, `is_quaint_active`, `is_sharing_active`, `is_triple_active`, `adault_partial_payment`, `child_partial_payment`, `infant_partial_payment`, `is_partial_payment_active`, `is_service_charge_active`, `adault_visa_price`, `child_visa_price`, `infant_visa_price`, `booked_seats`, `confirmed_seats`, `left_seats`, `inventory_owner_organization_id`) VALUES
(1, '21 days Umrah package', '', 14, 1, 0, 1, 0, 0, 1, 1, 1, 1, 5, 1010010, 5, 8, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 10000, 1000, 1000, 0, 0, 0, NULL),
(8, '21 DAYS UMRAH PACKAGE SHUTTLE SERVICE', '', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, NULL),
(9, 'UMRAH PACKAGE 22 DAYS', '', 10, 5, 5, 5, 10, 0, 10, 10, 10, 1, 9, 9, 9, 8, 1, 1, 1, 1, 1, 10, 10, 10, 0, 0, 100, 100, 100, 0, 0, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahpackagediscountdetails`
--

CREATE TABLE `packages_umrahpackagediscountdetails` (
  `id` bigint(20) NOT NULL,
  `adault_from` int(11) NOT NULL,
  `adault_to` int(11) NOT NULL,
  `max_discount` double NOT NULL,
  `package_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahpackagediscountdetails`
--

INSERT INTO `packages_umrahpackagediscountdetails` (`id`, `adault_from`, `adault_to`, `max_discount`, `package_id`) VALUES
(29, 1, 1, 1, 1),
(18, 1, 1, 1, 8),
(3, 1, 1, 1, 3),
(4, 1, 1, 1, 4),
(28, 29, 10, 9, 9);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahpackagehoteldetails`
--

CREATE TABLE `packages_umrahpackagehoteldetails` (
  `id` bigint(20) NOT NULL,
  `check_in_date` date DEFAULT NULL,
  `check_out_date` date DEFAULT NULL,
  `number_of_nights` int(11) NOT NULL,
  `hotel_id` bigint(20) NOT NULL,
  `package_id` bigint(20) NOT NULL,
  `double_bed_price` double NOT NULL,
  `quad_bed_price` double NOT NULL,
  `quaint_bed_price` double NOT NULL,
  `sharing_bed_price` double NOT NULL,
  `triple_bed_price` double NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahpackagehoteldetails`
--

INSERT INTO `packages_umrahpackagehoteldetails` (`id`, `check_in_date`, `check_out_date`, `number_of_nights`, `hotel_id`, `package_id`, `double_bed_price`, `quad_bed_price`, `quaint_bed_price`, `sharing_bed_price`, `triple_bed_price`) VALUES
(45, '2025-07-23', '2025-07-31', 8, 16, 1, 1000, 1000, 1000, 2000, 10000),
(44, '2025-08-01', '2025-08-09', 8, 13, 1, 10999, 9000, 10000, 8000, 12000),
(3, '2024-12-31', '2025-07-25', 206, 12, 3, 1, 1, 1, 1, 1),
(4, '2025-07-11', '2025-08-08', 28, 12, 4, 1, 1, 1, 1, 1),
(26, '2025-07-26', '2025-07-30', 4, 11, 8, 1, 1, 1, 1, 1),
(43, '2025-07-01', '2025-07-06', 5, 17, 9, 13, 11, 10, 10, 12);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahpackageticketdetails`
--

CREATE TABLE `packages_umrahpackageticketdetails` (
  `id` bigint(20) NOT NULL,
  `package_id` bigint(20) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahpackageticketdetails`
--

INSERT INTO `packages_umrahpackageticketdetails` (`id`, `package_id`, `ticket_id`) VALUES
(26, 1, 8),
(15, 8, 9),
(25, 9, 8);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahpackagetransportdetails`
--

CREATE TABLE `packages_umrahpackagetransportdetails` (
  `id` bigint(20) NOT NULL,
  `vehicle_type` int(11) DEFAULT NULL,
  `package_id` bigint(20) NOT NULL,
  `transport_sector_id` bigint(20) DEFAULT NULL,
  `transport_type` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahpackagetransportdetails`
--

INSERT INTO `packages_umrahpackagetransportdetails` (`id`, `vehicle_type`, `package_id`, `transport_sector_id`, `transport_type`) VALUES
(26, 0, 1, NULL, NULL),
(15, 0, 8, NULL, NULL),
(25, 0, 9, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahvisaprice`
--

CREATE TABLE `packages_umrahvisaprice` (
  `id` bigint(20) NOT NULL,
  `visa_type` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `adault_price` double NOT NULL,
  `child_price` double NOT NULL,
  `infant_price` double NOT NULL,
  `maximum_nights` int(11) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahvisaprice`
--

INSERT INTO `packages_umrahvisaprice` (`id`, `visa_type`, `category`, `adault_price`, `child_price`, `infant_price`, `maximum_nights`, `organization_id`) VALUES
(11, 'type1', 'short stay', 111, 1107, 1109, 0, 8),
(10, 'type1', 'long stay with hotel', 100, 110, 10188, 110, 8),
(8, 'type1', 'short stay with hotel', 1009, 200, 100, 10, 8),
(12, 'type1', 'long stay', 120000, 909, 1100, 0, 8);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahvisapricetwo`
--

CREATE TABLE `packages_umrahvisapricetwo` (
  `id` bigint(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `person_from` int(11) NOT NULL,
  `person_to` int(11) NOT NULL,
  `adault_price` double NOT NULL,
  `child_price` double NOT NULL,
  `infant_price` double NOT NULL,
  `is_transport` tinyint(1) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahvisapricetwo`
--

INSERT INTO `packages_umrahvisapricetwo` (`id`, `title`, `person_from`, `person_to`, `adault_price`, `child_price`, `infant_price`, `is_transport`, `organization_id`) VALUES
(2, '1-4 pex visa price', 1, 4, 850, 850, 491, 1, 8),
(3, '5-19 pex visa price', 5, 20, 595, 595, 490, 1, 8),
(4, '19-49 pex visa price', 19, 49, 585, 585, 490, 1, 8),
(5, '49-100', 49, 100, 200, 200, 200, 1, 8),
(6, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8),
(7, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8),
(8, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8),
(9, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8),
(10, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8),
(11, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8),
(12, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8),
(13, 'string', 2095419580, -1856882830, 5788.846508720285, 3660.279597205278, 1584.3408619847698, 1, 8);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahvisapricetwohotel`
--

CREATE TABLE `packages_umrahvisapricetwohotel` (
  `id` bigint(20) NOT NULL,
  `hotel_id` bigint(20) NOT NULL,
  `umrah_visa_price_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahvisapricetwohotel`
--

INSERT INTO `packages_umrahvisapricetwohotel` (`id`, `hotel_id`, `umrah_visa_price_id`) VALUES
(29, 13, 2),
(28, 16, 2),
(25, 11, 3),
(16, 11, 4),
(15, 12, 4),
(31, 16, 5);

-- --------------------------------------------------------

--
-- Table structure for table `packages_umrahvisapricetwo_vehicle_types`
--

CREATE TABLE `packages_umrahvisapricetwo_vehicle_types` (
  `id` bigint(20) NOT NULL,
  `umrahvisapricetwo_id` bigint(20) NOT NULL,
  `vehicletype_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_umrahvisapricetwo_vehicle_types`
--

INSERT INTO `packages_umrahvisapricetwo_vehicle_types` (`id`, `umrahvisapricetwo_id`, `vehicletype_id`) VALUES
(1, 11, 1),
(2, 12, 1),
(3, 13, 1),
(4, 13, 2),
(5, 2, 4),
(6, 2, 2),
(7, 5, 2),
(8, 5, 4);

-- --------------------------------------------------------

--
-- Table structure for table `packages_ziaratprice`
--

CREATE TABLE `packages_ziaratprice` (
  `id` bigint(20) NOT NULL,
  `ziarat_title` varchar(100) NOT NULL,
  `contact_person` varchar(100) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `price` double NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `city_id` bigint(20) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `max_pex` double NOT NULL,
  `min_pex` double NOT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `packages_ziaratprice`
--

INSERT INTO `packages_ziaratprice` (`id`, `ziarat_title`, `contact_person`, `contact_number`, `price`, `organization_id`, `city_id`, `description`, `max_pex`, `min_pex`, `status`) VALUES
(1, 'Makkah-Sites', 'Mubeen', '1234567890', 10000, 8, 19, '', 0, 0, 'active'),
(3, 'ziarat', 'sasdsdasdas', '909090', 6914.997512412464, 8, NULL, NULL, 0, 0, 'active'),
(4, 'ziarat', 'sasdsdasdas', '909090', 6914.997512412464, 8, 5, 'this is for testing purpose', 0, 0, 'active'),
(5, 'ziarat', 'sasdsdasdas', '909090', 6914.997512412464, 8, NULL, 'this is for testing purpose', 0, 0, 'active'),
(6, 'ziarat', 'sasdsdasdas', '909090', 6914.997512412464, 8, 5, 'this is for testing purpose', 0, 0, 'active'),
(7, 'ziarat', 'sasdsdasdas', '909090', 6914.997512412464, 8, 5, 'this is for testing purpose', 0, 0, 'active'),
(8, 'ziarat', 'sasdsdasdas', '909090', 6914.997512412464, 8, 5, 'this is for testing purpose', 0, 0, 'active'),
(9, 'ziarat', 'sasdsdasdas', '909090', 6914.997512412464, 8, 18, 'this is for testing purpose', 0, 0, 'inactive'),
(10, 'Road Site', 'mubeen', '1234567890', 100, 8, 20, 'Road Site for 2', 10, 1, 'active');

-- --------------------------------------------------------

--
-- Table structure for table `small_sector`
--

CREATE TABLE `small_sector` (
  `id` bigint(20) NOT NULL,
  `contact_name` varchar(100) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `arrival_city_id` bigint(20) DEFAULT NULL,
  `departure_city_id` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `small_sector`
--

INSERT INTO `small_sector` (`id`, `contact_name`, `contact_number`, `organization_id`, `arrival_city_id`, `departure_city_id`) VALUES
(8, '1234567890', 'Raza', 8, 16, 19),
(7, '1234567890', 'ali', 8, 19, 20),
(6, 'Mubeen', '1234567890', 8, 16, 15),
(9, 'ahsan', '1234567890', 8, 19, 16),
(10, 'ahsan', '1234567890', 8, 20, 19);

-- --------------------------------------------------------

--
-- Table structure for table `tickets_hotelcontactdetails`
--

CREATE TABLE `tickets_hotelcontactdetails` (
  `id` bigint(20) NOT NULL,
  `contact_person` varchar(100) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `hotel_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tickets_hotelcontactdetails`
--

INSERT INTO `tickets_hotelcontactdetails` (`id`, `contact_person`, `contact_number`, `hotel_id`) VALUES
(17, 'Mubeen Abbas', '123456789012', 14),
(19, 'Malik', '1234567890', 15),
(22, 'daniyal', '234567890', 16),
(21, 'Ahsan', '1234567890', 17),
(20, 'malik sb', '1234567890', 18),
(9, 'string', 'string', 19),
(10, 'string', 'string', 19),
(11, 'string', 'string', 20),
(12, 'string', 'string', 20),
(13, 'string', 'string', 21),
(14, 'string', 'string', 21),
(16, 'mubeen', '1234567890', 22);

-- --------------------------------------------------------

--
-- Table structure for table `tickets_hotelprices`
--

CREATE TABLE `tickets_hotelprices` (
  `id` bigint(20) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `room_type` varchar(50) NOT NULL,
  `hotel_id` bigint(20) NOT NULL,
  `is_sharing_allowed` tinyint(1) NOT NULL,
  `price` double NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tickets_hotelprices`
--

INSERT INTO `tickets_hotelprices` (`id`, `start_date`, `end_date`, `room_type`, `hotel_id`, `is_sharing_allowed`, `price`) VALUES
(138, '2025-09-19', '2025-09-20', 'Sharing', 13, 1, 10000),
(53, '2025-08-01', '2025-08-31', 'Sharing', 12, 0, 0),
(57, '2025-08-01', '2025-08-15', 'Sharing', 11, 0, 0),
(56, '2025-08-16', '2025-08-31', 'Only-Room', 11, 0, 0),
(58, '2025-08-01', '2025-09-01', 'Only-Room', 14, 0, 1000),
(59, '2025-08-02', '2025-09-02', 'Sharing', 15, 1, 1000),
(60, '2025-08-02', '2025-09-02', 'Double Bed', 15, 1, 400),
(61, '2025-08-02', '2025-09-02', 'Triple Bed', 15, 1, 493),
(91, '2025-08-02', '2025-08-25', 'Only-Room', 16, 0, 10500),
(89, '2025-08-26', '2025-09-02', 'Quint Bed', 16, 1, 794),
(90, '2025-08-26', '2025-09-02', 'Double Bed', 16, 1, 497),
(88, '2025-08-26', '2025-09-02', 'Quad Bed', 16, 1, 600),
(87, '2025-08-26', '2025-09-02', 'Triple Bed', 16, 1, 400),
(86, '2025-08-26', '2025-09-02', 'Sharing', 16, 1, 500),
(80, '2025-08-02', '2025-08-30', 'Only-Room', 17, 0, 1040),
(81, '2025-08-31', '2025-09-02', 'Sharing', 17, 1, 500),
(139, '2025-07-30', '2025-09-11', 'Only-Room', 13, 0, 10),
(131, '2025-08-01', '2025-08-31', 'Double Bed', 18, 0, 2500),
(132, '2025-08-01', '2025-08-31', 'Triple Bed', 18, 0, 3000),
(130, '2025-08-01', '2025-08-31', 'Sharing', 18, 1, 2000),
(129, '2025-08-01', '2025-08-31', 'Only-Room', 18, 1, 2000),
(128, '2025-09-01', '2025-09-30', 'Triple Bed', 18, 0, 3000),
(126, '2025-09-01', '2025-09-30', 'Sharing', 18, 1, 2500),
(127, '2025-09-01', '2025-09-30', 'Double Bed', 18, 0, 2600),
(125, '2025-09-01', '2025-09-30', 'Only-Room', 18, 1, 2500),
(137, '2025-09-19', '2025-09-20', 'Only-Room', 13, 1, 100),
(140, '2025-09-12', '2025-09-18', 'Only-Room', 13, 1, 1000),
(141, '2025-09-12', '2025-09-18', 'Sharing', 13, 1, 100),
(142, '1963-04-03', '1961-04-13', 'string', 19, 0, 1601.5393779629217),
(143, '2008-09-13', '2004-04-18', 'string', 19, 1, 6144.197999114746),
(144, '1963-04-03', '1961-04-13', 'string', 20, 0, 1601.5393779629217),
(145, '2008-09-13', '2004-04-18', 'string', 20, 1, 6144.197999114746),
(146, '1963-04-03', '1961-04-13', 'string', 21, 0, 1601.5393779629217),
(147, '2008-09-13', '2004-04-18', 'string', 21, 1, 6144.197999114746),
(148, '2025-09-24', '2025-11-22', 'Only-Room', 22, 0, 1000);

-- --------------------------------------------------------

--
-- Table structure for table `tickets_hotelrooms`
--

CREATE TABLE `tickets_hotelrooms` (
  `id` bigint(20) NOT NULL,
  `floor` varchar(50) NOT NULL,
  `room_type` varchar(50) NOT NULL,
  `room_number` varchar(20) NOT NULL,
  `total_beds` int(11) NOT NULL,
  `hotel_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tickets_hotels`
--

CREATE TABLE `tickets_hotels` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` longtext NOT NULL,
  `google_location` varchar(255) DEFAULT NULL,
  `google_drive_link` varchar(255) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `category` varchar(50) NOT NULL,
  `distance` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `available_start_date` date NOT NULL,
  `available_end_date` date NOT NULL,
  `city_id` bigint(20) DEFAULT NULL,
  `organization_id` bigint(20) NOT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tickets_hotels`
--

INSERT INTO `tickets_hotels` (`id`, `name`, `address`, `google_location`, `google_drive_link`, `contact_number`, `category`, `distance`, `is_active`, `available_start_date`, `available_end_date`, `city_id`, `organization_id`, `status`) VALUES
(16, 'Multan', 'main road', 'main road', 'main road', '1234567890', '4 Star', 110, 1, '2025-08-02', '2025-09-02', 18, 8, NULL),
(11, 'Saif ul majd', 'Hijra Road', 'WWW.google.com', 'www.google.com', '03000709017', '1 Star', 651, 1, '2025-08-01', '2025-08-31', 19, 8, NULL),
(13, 'DIWAN AL BAIT', 'GANNA WALI GALI', 'GANA WLAI GALI', 'GANA WALI GALI', '03000709017', 'ECO', 101, 1, '2025-07-30', '2025-09-20', 20, 8, NULL),
(14, 'Hilton', 'Ibrahim Al Khalil Rd,', 'Ibrahim Al Khalil Rd', 'Ibrahim Al Khalil Rd, Jabal Omar, Makkah 21955, Saudi Arabia', '1234567890', '5 Star', 10, 1, '2025-08-01', '2025-09-01', 19, 8, NULL),
(17, 'Saif ul Majd', 'main road', 'main road', 'main road', '1234567890', '5 Star', 110, 1, '2025-08-02', '2025-09-02', 20, 8, NULL),
(15, 'Al Arabia', 'Main Road', 'Main Road', 'Main Road', '1234567890', '4 Star', 120, 1, '2025-08-02', '2025-09-02', 20, 8, NULL),
(18, 'Malik Hotel', 'main road', 'main road', 'main road', '1234567890', '5 Star', 110, 1, '2025-08-01', '2025-09-30', 19, 8, NULL),
(22, 'PC', 'jakfja', 'jdkfaj', 'jdklfja', '1234567890', '5 Star', 100, 1, '2025-09-24', '2025-11-22', 21, 8, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tickets_roomdetails`
--

CREATE TABLE `tickets_roomdetails` (
  `id` bigint(20) NOT NULL,
  `bed_number` varchar(20) NOT NULL,
  `is_assigned` tinyint(1) NOT NULL,
  `room_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tickets_tickerstopoverdetails`
--

CREATE TABLE `tickets_tickerstopoverdetails` (
  `id` bigint(20) NOT NULL,
  `stopover_duration` varchar(100) NOT NULL,
  `trip_type` varchar(50) NOT NULL,
  `stopover_city_id` bigint(20) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tickets_tickerstopoverdetails`
--

INSERT INTO `tickets_tickerstopoverdetails` (`id`, `stopover_duration`, `trip_type`, `stopover_city_id`, `ticket_id`) VALUES
(36, '120', 'Return', 17, 8),
(9, '120', 'Departure', 18, 7),
(35, '120', 'Departure', 17, 8),
(12, '150', 'Departure', 7, 12),
(13, '20', 'Departure', 7, 13),
(14, '20', 'Departure', 6, 14),
(15, '20', 'Departure', 6, 15),
(16, '130', 'Return', 8, 15);

-- --------------------------------------------------------

--
-- Table structure for table `tickets_ticket`
--

CREATE TABLE `tickets_ticket` (
  `id` bigint(20) NOT NULL,
  `is_meal_included` tinyint(1) NOT NULL,
  `is_refundable` tinyint(1) NOT NULL,
  `pnr` varchar(100) NOT NULL,
  `total_seats` int(11) NOT NULL,
  `weight` double NOT NULL,
  `pieces` int(11) NOT NULL,
  `is_umrah_seat` tinyint(1) NOT NULL,
  `trip_type` varchar(50) NOT NULL,
  `departure_stay_type` varchar(50) NOT NULL,
  `return_stay_type` varchar(50) NOT NULL,
  `airline_id` bigint(20) NOT NULL,
  `organization_id` bigint(20) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `adult_price` double NOT NULL,
  `child_price` double NOT NULL,
  `infant_price` double NOT NULL,
  `booked_tickets` int(11) NOT NULL,
  `confirmed_tickets` int(11) NOT NULL,
  `left_seats` int(11) NOT NULL,
  `inventory_owner_organization_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tickets_ticket`
--

INSERT INTO `tickets_ticket` (`id`, `is_meal_included`, `is_refundable`, `pnr`, `total_seats`, `weight`, `pieces`, `is_umrah_seat`, `trip_type`, `departure_stay_type`, `return_stay_type`, `airline_id`, `organization_id`, `status`, `adult_price`, `child_price`, `infant_price`, `booked_tickets`, `confirmed_tickets`, `left_seats`, `inventory_owner_organization_id`) VALUES
(8, 0, 0, '12', 12, 40, 2, 0, 'Round-trip', '1-Stop', '1-Stop', 15, 8, NULL, 120000, 100000, 80000, 0, 0, 12, NULL),
(5, 0, 1, 'Hy', 20, 30, 2, 0, 'One-way', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 0, 0, 0, 0, 0, 0, NULL),
(6, 1, 1, 'hy', 30, 30, 2, 1, 'One-way', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 0, 0, 0, 0, 0, 0, NULL),
(7, 1, 0, 'ji', 10, 10, 2, 1, 'One-way', '1-Stop', 'Non-Stop', 14, 8, NULL, 0, 0, 0, 0, 0, 0, NULL),
(9, 1, 1, '123456', 30, 30, 2, 1, 'One-way', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 0, 0, 0, 0, 0, 0, NULL),
(10, 0, 0, 'Hehd', 20, 40, 1, 0, 'One-way', 'Non-Stop', 'Non-Stop', 16, 7, NULL, 0, 0, 0, 0, 0, 0, NULL),
(11, 0, 0, 'Hehd', 20, 40, 1, 0, 'One-way', 'Non-Stop', 'Non-Stop', 16, 7, NULL, 0, 0, 0, 0, 0, 0, NULL),
(12, 0, 0, 'Hehd', 20, 40, 1, 0, 'One-way', '1-Stop', 'Non-Stop', 16, 7, NULL, 0, 0, 0, 0, 0, 0, NULL),
(13, 0, 0, 'Hehd', 20, 40, 1, 0, 'One-way', '1-Stop', 'Non-Stop', 16, 7, NULL, 0, 0, 0, 0, 0, 0, NULL),
(14, 0, 0, 'Hehd', 20, 40, 1, 0, 'Round-trip', '1-Stop', 'Non-Stop', 16, 7, NULL, 0, 0, 0, 0, 0, 0, NULL),
(15, 0, 0, 'Hehd', 20, 40, 1, 0, 'Round-trip', '1-Stop', '1-Stop', 16, 7, NULL, 0, 0, 0, 0, 0, 0, NULL),
(16, 0, 1, '123456789', 12, 2, 1, 1, 'One-way', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 120, 100, 0, 0, 0, 0, NULL),
(17, 0, 0, '565', 10, 22, 2, 1, 'One-way', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 0, 0, 0, 0, 0, 0, NULL),
(18, 1, 1, '1', 1, 1, 1, 1, 'One-way', 'Non-Stop', 'Non-Stop', 15, 8, NULL, 1, 1, 1, 0, 0, 0, NULL),
(19, 0, 0, 'Okshs', 20, 10, 1, 0, 'One-way', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 120, 100, 90, 0, 0, 0, NULL),
(20, 1, 0, '2936', 279, 987, 89, 1, 'Round-trip', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 987, 789, 0, 0, 0, 0, NULL),
(21, 1, 1, '232', 23, 23, 2, 1, 'Round-trip', 'Non-Stop', 'Non-Stop', 14, 8, NULL, 922, 29, 292, 0, 0, 0, NULL),
(22, 1, 1, '122ee', 20, 30, 2, 1, 'Round-trip', 'Non-Stop', 'Non-Stop', 15, 8, NULL, 150000, 120000, 80000, 0, 0, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tickets_tickettripdetails`
--

CREATE TABLE `tickets_tickettripdetails` (
  `id` bigint(20) NOT NULL,
  `departure_date_time` datetime(6) NOT NULL,
  `arrival_date_time` datetime(6) NOT NULL,
  `trip_type` varchar(50) NOT NULL,
  `arrival_city_id` bigint(20) NOT NULL,
  `departure_city_id` bigint(20) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tickets_tickettripdetails`
--

INSERT INTO `tickets_tickettripdetails` (`id`, `departure_date_time`, `arrival_date_time`, `trip_type`, `arrival_city_id`, `departure_city_id`, `ticket_id`) VALUES
(71, '2025-07-10 09:08:00.000000', '2025-07-10 11:09:00.000000', 'Return', 16, 18, 8),
(70, '2025-07-20 18:03:00.000000', '2025-07-19 23:09:00.000000', 'Departure', 18, 20, 8),
(20, '2025-07-09 08:53:00.000000', '2025-07-08 08:53:00.000000', 'Departure', 17, 18, 5),
(8, '2025-07-17 17:53:00.000000', '2025-07-09 17:53:00.000000', 'Departure', 17, 18, 6),
(15, '2025-07-10 17:58:00.000000', '2025-07-25 17:59:00.000000', 'Departure', 17, 18, 7),
(21, '2025-07-08 18:30:00.000000', '2025-07-08 18:30:00.000000', 'Departure', 8, 5, 10),
(19, '2025-07-02 05:08:00.000000', '2025-07-02 05:09:00.000000', 'Departure', 16, 15, 9),
(22, '2025-07-08 18:30:00.000000', '2025-07-08 18:30:00.000000', 'Departure', 8, 5, 11),
(23, '2025-07-08 18:30:00.000000', '2025-07-08 18:30:00.000000', 'Departure', 8, 5, 12),
(24, '2025-07-08 18:30:00.000000', '2025-07-08 18:30:00.000000', 'Departure', 8, 5, 13),
(25, '2025-07-08 18:30:00.000000', '2025-07-08 18:30:00.000000', 'Departure', 8, 5, 14),
(26, '2025-07-08 18:30:00.000000', '2025-07-09 18:30:00.000000', 'Return', 7, 5, 14),
(27, '2025-07-08 18:30:00.000000', '2025-07-08 18:30:00.000000', 'Departure', 8, 5, 15),
(28, '2025-07-08 18:30:00.000000', '2025-07-09 18:30:00.000000', 'Return', 7, 5, 15),
(55, '2025-07-10 08:08:00.000000', '2025-07-09 12:08:00.000000', 'Departure', 20, 21, 16),
(49, '2025-07-25 05:02:00.000000', '2025-07-26 05:02:00.000000', 'Departure', 19, 20, 17),
(52, '2025-07-26 04:33:00.000000', '2025-07-28 04:33:00.000000', 'Departure', 16, 15, 18),
(53, '2025-07-28 23:55:00.000000', '2025-07-28 23:55:00.000000', 'Departure', 15, 16, 19),
(56, '2025-07-03 12:54:00.000000', '2025-07-04 12:58:00.000000', 'Departure', 18, 20, 20),
(57, '2025-09-25 12:54:00.000000', '2025-09-29 12:00:00.000000', 'Return', 17, 19, 20),
(58, '2025-08-03 12:43:00.000000', '2025-08-14 12:40:00.000000', 'Departure', 18, 17, 21),
(59, '2025-08-03 04:40:00.000000', '2025-08-14 12:44:00.000000', 'Return', 18, 17, 21),
(69, '2025-09-30 20:53:00.000000', '2025-10-01 00:53:00.000000', 'Return', 15, 16, 22),
(68, '2025-09-01 20:05:00.000000', '2025-09-02 05:50:00.000000', 'Departure', 16, 15, 22);

-- --------------------------------------------------------

--
-- Table structure for table `users_groupextension`
--

CREATE TABLE `users_groupextension` (
  `id` bigint(20) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `group_id` int(11) NOT NULL,
  `organization_id` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users_groupextension`
--

INSERT INTO `users_groupextension` (`id`, `type`, `group_id`, `organization_id`) VALUES
(19, 'employee', 19, 8),
(20, 'employee', 20, 7),
(21, 'agents', 21, 8),
(22, 'agent', 22, 7),
(24, 'agents', 24, 8);

-- --------------------------------------------------------

--
-- Table structure for table `users_permissionextension`
--

CREATE TABLE `users_permissionextension` (
  `id` bigint(20) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users_permissionextension`
--

INSERT INTO `users_permissionextension` (`id`, `type`, `permission_id`) VALUES
(2, 'default', 45),
(5, 'default', 54),
(4, 'default', 53);

-- --------------------------------------------------------

--
-- Table structure for table `users_userprofile`
--

CREATE TABLE `users_userprofile` (
  `id` bigint(20) NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users_userprofile`
--

INSERT INTO `users_userprofile` (`id`, `type`, `user_id`) VALUES
(20, 'agent', 20),
(21, 'employee', 21),
(24, 'subagent', 24),
(33, 'employee', 34),
(29, 'agent', 29),
(30, 'agent', 30),
(32, 'subagent', 32);

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_type`
--

CREATE TABLE `vehicle_type` (
  `id` bigint(20) NOT NULL,
  `vehicle_name` varchar(100) NOT NULL,
  `vehicle_type` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `note` longtext DEFAULT NULL,
  `visa_type` varchar(100) NOT NULL,
  `status` varchar(10) NOT NULL,
  `big_sector_id` bigint(20) DEFAULT NULL,
  `organization_id` bigint(20) NOT NULL,
  `small_sector_id` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `vehicle_type`
--

INSERT INTO `vehicle_type` (`id`, `vehicle_name`, `vehicle_type`, `price`, `note`, `visa_type`, `status`, `big_sector_id`, `organization_id`, `small_sector_id`) VALUES
(1, 'Toyota Hiace', 'Van', 5000.00, 'For school transport', 'type2', 'inactive', NULL, 8, 10),
(2, 'Toyota Hiace', 'Van', 5000.00, 'For school transport', 'type2', 'active', NULL, 8, 8),
(4, 'Toyota Revo (GR)', 'Jeep', 500.00, 'New Condition', 'type2', 'active', 14, 8, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  ADD KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  ADD KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  ADD KEY `auth_user_groups_group_id_97559544` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  ADD KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`);

--
-- Indexes for table `big_sector`
--
ALTER TABLE `big_sector`
  ADD PRIMARY KEY (`id`),
  ADD KEY `big_sector_organization_id_76ace7db` (`organization_id`);

--
-- Indexes for table `big_sector_small_sectors`
--
ALTER TABLE `big_sector_small_sectors`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `booking_bigsector_small__bigsector_id_sector_id_9f68315b_uniq` (`bigsector_id`,`sector_id`),
  ADD KEY `booking_bigsector_small_sectors_bigsector_id_2e7a77d2` (`bigsector_id`),
  ADD KEY `booking_bigsector_small_sectors_sector_id_98251233` (`sector_id`);

--
-- Indexes for table `booking_allowedreseller`
--
ALTER TABLE `booking_allowedreseller`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_allowedreseller_inventory_owner_company_id_0f6e60c0` (`inventory_owner_company_id`);

--
-- Indexes for table `booking_allowedreseller_reseller_companies`
--
ALTER TABLE `booking_allowedreseller_reseller_companies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `booking_allowedreseller__allowedreseller_id_organ_87fbff18_uniq` (`allowedreseller_id`,`organization_id`),
  ADD KEY `booking_allowedreseller_res_allowedreseller_id_f15f3a27` (`allowedreseller_id`),
  ADD KEY `booking_allowedreseller_res_organization_id_98f522c8` (`organization_id`);

--
-- Indexes for table `booking_bank`
--
ALTER TABLE `booking_bank`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bank_organization_id_96e441ef` (`organization_id`);

--
-- Indexes for table `booking_bankaccount`
--
ALTER TABLE `booking_bankaccount`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `iban` (`iban`),
  ADD KEY `booking_bankaccount_agency_id_37dd2b74` (`agency_id`),
  ADD KEY `booking_bankaccount_branch_id_4c9e7c91` (`branch_id`),
  ADD KEY `booking_bankaccount_organization_id_ba999143` (`organization_id`);

--
-- Indexes for table `booking_booking`
--
ALTER TABLE `booking_booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_booking_agency_id_d8a674ce` (`agency_id`),
  ADD KEY `booking_booking_branch_id_477bde60` (`branch_id`),
  ADD KEY `booking_booking_organization_id_091710e4` (`organization_id`),
  ADD KEY `booking_booking_user_id_e1eb6912` (`user_id`),
  ADD KEY `booking_booking_umrah_package_id_4eba26f9` (`umrah_package_id`),
  ADD KEY `booking_booking_rejected_employer_id_76d3aa9d` (`rejected_employer_id`),
  ADD KEY `booking_booking_confirmed_by_id_3973acac` (`confirmed_by_id`);

--
-- Indexes for table `booking_bookinghoteldetails`
--
ALTER TABLE `booking_bookinghoteldetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookinghoteldetails_booking_id_2f080b70` (`booking_id`),
  ADD KEY `booking_bookinghoteldetails_hotel_id_40a9dc68` (`hotel_id`);

--
-- Indexes for table `booking_bookingpersoncontactdetails`
--
ALTER TABLE `booking_bookingpersoncontactdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingpersoncontactdetails_person_id_870cc53f` (`person_id`);

--
-- Indexes for table `booking_bookingpersondetail`
--
ALTER TABLE `booking_bookingpersondetail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingpersondetail_booking_id_c9785972` (`booking_id`),
  ADD KEY `booking_bookingpersondetail_shirka_id_952df901` (`shirka_id`);

--
-- Indexes for table `booking_bookingpersonfooddetails`
--
ALTER TABLE `booking_bookingpersonfooddetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingpersonfooddetails_person_id_9f654e03` (`person_id`);

--
-- Indexes for table `booking_bookingpersonziyaratdetails`
--
ALTER TABLE `booking_bookingpersonziyaratdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingpersonziyaratdetails_person_id_887101bc` (`person_id`);

--
-- Indexes for table `booking_bookingticketdetails`
--
ALTER TABLE `booking_bookingticketdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingticketdetails_booking_id_b8b586be` (`booking_id`),
  ADD KEY `booking_bookingticketdetails_ticket_id_4ac1dc95` (`ticket_id`);

--
-- Indexes for table `booking_bookingticketstopoverdetails`
--
ALTER TABLE `booking_bookingticketstopoverdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingticketstopoverdetails_stopover_city_id_624d14af` (`stopover_city_id`),
  ADD KEY `booking_bookingticketstopoverdetails_ticket_id_96b16ece` (`ticket_id`);

--
-- Indexes for table `booking_bookingtickettickettripdetails`
--
ALTER TABLE `booking_bookingtickettickettripdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingtickettickettripdetails_arrival_city_id_1d40fefa` (`arrival_city_id`),
  ADD KEY `booking_bookingticketticket_departure_city_id_042ec8b2` (`departure_city_id`),
  ADD KEY `booking_bookingtickettickettripdetails_ticket_id_4532c2fb` (`ticket_id`);

--
-- Indexes for table `booking_bookingtransportdetails`
--
ALTER TABLE `booking_bookingtransportdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingtransportdetails_booking_id_3a074f45` (`booking_id`),
  ADD KEY `booking_bookingtransportdetails_shirka_id_e77c8163` (`shirka_id`),
  ADD KEY `booking_bookingtransportdetails_vehicle_type_id_a96d9fdd` (`vehicle_type_id`);

--
-- Indexes for table `booking_bookingtransportsector`
--
ALTER TABLE `booking_bookingtransportsector`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_bookingtransportsector_transport_detail_id_5a454f99` (`transport_detail_id`);

--
-- Indexes for table `booking_booking_internals`
--
ALTER TABLE `booking_booking_internals`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `booking_booking_internal_booking_id_internalnote__47ed3a63_uniq` (`booking_id`,`internalnote_id`),
  ADD KEY `booking_booking_internals_booking_id_dfff1845` (`booking_id`),
  ADD KEY `booking_booking_internals_internalnote_id_097f55f3` (`internalnote_id`);

--
-- Indexes for table `booking_discount`
--
ALTER TABLE `booking_discount`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_discount_discount_group_id_48409ada` (`discount_group_id`),
  ADD KEY `booking_discount_organization_id_8e242c54` (`organization_id`);

--
-- Indexes for table `booking_discountgroup`
--
ALTER TABLE `booking_discountgroup`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_discountgroup_organization_id_79222bf3` (`organization_id`);

--
-- Indexes for table `booking_internalnote`
--
ALTER TABLE `booking_internalnote`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_internalnote_employee_id_aa3c550b` (`employee_id`);

--
-- Indexes for table `booking_markup`
--
ALTER TABLE `booking_markup`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `booking_organizationlink`
--
ALTER TABLE `booking_organizationlink`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `booking_payment`
--
ALTER TABLE `booking_payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_payment_agency_id_eda9a980` (`agency_id`),
  ADD KEY `booking_payment_agent_id_8aaff034` (`agent_id`),
  ADD KEY `booking_payment_bank_id_e1be9702` (`bank_id`),
  ADD KEY `booking_payment_booking_id_dd24b13e` (`booking_id`),
  ADD KEY `booking_payment_branch_id_a3371fea` (`branch_id`),
  ADD KEY `booking_payment_created_by_id_5be99535` (`created_by_id`),
  ADD KEY `booking_payment_organization_id_89a5e08d` (`organization_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `organization_agency`
--
ALTER TABLE `organization_agency`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_agency_branch_id_8bdde094` (`branch_id`);

--
-- Indexes for table `organization_agencycontact`
--
ALTER TABLE `organization_agencycontact`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_agencycontact_agency_id_7f340db7` (`agency_id`);

--
-- Indexes for table `organization_agencyfiles`
--
ALTER TABLE `organization_agencyfiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_agencyfiles_agency_id_c0412f8e` (`agency_id`);

--
-- Indexes for table `organization_agency_user`
--
ALTER TABLE `organization_agency_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `organization_agency_user_agency_id_user_id_f1ddd71b_uniq` (`agency_id`,`user_id`),
  ADD KEY `organization_agency_user_agency_id_c88ffba9` (`agency_id`),
  ADD KEY `organization_agency_user_user_id_4488a223` (`user_id`);

--
-- Indexes for table `organization_branch`
--
ALTER TABLE `organization_branch`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_branch_organization_id_29d65229` (`organization_id`);

--
-- Indexes for table `organization_branch_user`
--
ALTER TABLE `organization_branch_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `organization_branch_user_branch_id_user_id_5102dfac_uniq` (`branch_id`,`user_id`),
  ADD KEY `organization_branch_user_branch_id_643ec00b` (`branch_id`),
  ADD KEY `organization_branch_user_user_id_40f5afa2` (`user_id`);

--
-- Indexes for table `organization_organization`
--
ALTER TABLE `organization_organization`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `organization_organization_user`
--
ALTER TABLE `organization_organization_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `organization_organizatio_organization_id_user_id_6b25971c_uniq` (`organization_id`,`user_id`),
  ADD KEY `organization_organization_user_organization_id_1885ec70` (`organization_id`),
  ADD KEY `organization_organization_user_user_id_29b63f3c` (`user_id`);

--
-- Indexes for table `packages_airlines`
--
ALTER TABLE `packages_airlines`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_airlines_organization_id_d19467b3` (`organization_id`);

--
-- Indexes for table `packages_bookingexpiry`
--
ALTER TABLE `packages_bookingexpiry`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_bookingexpiry_organization_id_b088f290` (`organization_id`);

--
-- Indexes for table `packages_city`
--
ALTER TABLE `packages_city`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_city_organization_id_709c57b1` (`organization_id`);

--
-- Indexes for table `packages_customumrahfooddetails`
--
ALTER TABLE `packages_customumrahfooddetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_customumrahfooddetails_food_id_d4d33791` (`food_id`),
  ADD KEY `packages_customumrahfooddetails_package_id_d2b7e0b3` (`package_id`);

--
-- Indexes for table `packages_customumrahpackage`
--
ALTER TABLE `packages_customumrahpackage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_customumrahpackage_organization_id_28b1cc0c` (`organization_id`),
  ADD KEY `packages_customumrahpackage_agency_id_6a0a08d0` (`agency_id`),
  ADD KEY `packages_customumrahpackage_user_id_5c97a485` (`user_id`);

--
-- Indexes for table `packages_customumrahpackagehoteldetails`
--
ALTER TABLE `packages_customumrahpackagehoteldetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_customumrahpackagehoteldetails_hotel_id_a0fdbfa9` (`hotel_id`),
  ADD KEY `packages_customumrahpackagehoteldetails_package_id_0165fd7c` (`package_id`);

--
-- Indexes for table `packages_customumrahpackageticketdetails`
--
ALTER TABLE `packages_customumrahpackageticketdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_customumrahpackageticketdetails_package_id_bf8042b5` (`package_id`),
  ADD KEY `packages_customumrahpackageticketdetails_ticket_id_e2be668c` (`ticket_id`);

--
-- Indexes for table `packages_customumrahpackagetransportdetails`
--
ALTER TABLE `packages_customumrahpackagetransportdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_customumrahpackagetransportdetails_package_id_8fb6b084` (`package_id`);

--
-- Indexes for table `packages_customumrahziaratdetails`
--
ALTER TABLE `packages_customumrahziaratdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_customumrahziaratdetails_package_id_ceea1399` (`package_id`),
  ADD KEY `packages_customumrahziaratdetails_ziarat_id_b6a7155d` (`ziarat_id`);

--
-- Indexes for table `packages_foodprice`
--
ALTER TABLE `packages_foodprice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_foodprice_organization_id_6d2ba71b` (`organization_id`),
  ADD KEY `packages_foodprice_city_id_aa0fe172` (`city_id`);

--
-- Indexes for table `packages_onlyvisaprice`
--
ALTER TABLE `packages_onlyvisaprice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_onlyvisaprice_organization_id_dcdaae1b` (`organization_id`),
  ADD KEY `packages_onlyvisaprice_city_id_70e33c00` (`city_id`);

--
-- Indexes for table `packages_riyalrate`
--
ALTER TABLE `packages_riyalrate`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `organization_id` (`organization_id`);

--
-- Indexes for table `packages_setvisatype`
--
ALTER TABLE `packages_setvisatype`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_setvisatype_organization_id_97eba0c6` (`organization_id`);

--
-- Indexes for table `packages_shirka`
--
ALTER TABLE `packages_shirka`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_shirka_organization_id_bab91554` (`organization_id`);

--
-- Indexes for table `packages_transportsectorprice`
--
ALTER TABLE `packages_transportsectorprice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_transportsectorprice_organization_id_ca5b8109` (`organization_id`);

--
-- Indexes for table `packages_umrahpackage`
--
ALTER TABLE `packages_umrahpackage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahpackage_organization_id_d2259e58` (`organization_id`);

--
-- Indexes for table `packages_umrahpackagediscountdetails`
--
ALTER TABLE `packages_umrahpackagediscountdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahpackagediscountdetails_package_id_4591e953` (`package_id`);

--
-- Indexes for table `packages_umrahpackagehoteldetails`
--
ALTER TABLE `packages_umrahpackagehoteldetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahpackagehoteldetails_hotel_id_e18ce34f` (`hotel_id`),
  ADD KEY `packages_umrahpackagehoteldetails_package_id_33b3e7b6` (`package_id`);

--
-- Indexes for table `packages_umrahpackageticketdetails`
--
ALTER TABLE `packages_umrahpackageticketdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahpackageticketdetails_package_id_82a58301` (`package_id`),
  ADD KEY `packages_umrahpackageticketdetails_ticket_id_2771fd62` (`ticket_id`);

--
-- Indexes for table `packages_umrahpackagetransportdetails`
--
ALTER TABLE `packages_umrahpackagetransportdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahpackagetransportdetails_package_id_ac755fe8` (`package_id`),
  ADD KEY `packages_umrahpackagetransp_transport_sector_id_df021b32` (`transport_sector_id`);

--
-- Indexes for table `packages_umrahvisaprice`
--
ALTER TABLE `packages_umrahvisaprice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahvisaprice_organization_id_444783f6` (`organization_id`);

--
-- Indexes for table `packages_umrahvisapricetwo`
--
ALTER TABLE `packages_umrahvisapricetwo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahvisapricetwo_organization_id_c1887ff9` (`organization_id`);

--
-- Indexes for table `packages_umrahvisapricetwohotel`
--
ALTER TABLE `packages_umrahvisapricetwohotel`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_umrahvisapricetwohotel_hotel_id_6d66e72c` (`hotel_id`),
  ADD KEY `packages_umrahvisapricetwohotel_umrah_visa_price_id_86d93f86` (`umrah_visa_price_id`);

--
-- Indexes for table `packages_umrahvisapricetwo_vehicle_types`
--
ALTER TABLE `packages_umrahvisapricetwo_vehicle_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `packages_umrahvisapricet_umrahvisapricetwo_id_veh_c8f16b24_uniq` (`umrahvisapricetwo_id`,`vehicletype_id`),
  ADD KEY `packages_umrahvisapricetwo__umrahvisapricetwo_id_96c81b27` (`umrahvisapricetwo_id`),
  ADD KEY `packages_umrahvisapricetwo_vehicle_types_vehicletype_id_e1da8eda` (`vehicletype_id`);

--
-- Indexes for table `packages_ziaratprice`
--
ALTER TABLE `packages_ziaratprice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `packages_ziaratprice_organization_id_9741d633` (`organization_id`),
  ADD KEY `packages_ziaratprice_city_id_26bddefa` (`city_id`);

--
-- Indexes for table `small_sector`
--
ALTER TABLE `small_sector`
  ADD PRIMARY KEY (`id`),
  ADD KEY `small_sector_organization_id_1134bcfa` (`organization_id`),
  ADD KEY `small_sector_arrival_city_id_b6297012` (`arrival_city_id`),
  ADD KEY `small_sector_departure_city_id_04cb2865` (`departure_city_id`);

--
-- Indexes for table `tickets_hotelcontactdetails`
--
ALTER TABLE `tickets_hotelcontactdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_hotelcontactdetails_hotel_id_994e3706` (`hotel_id`);

--
-- Indexes for table `tickets_hotelprices`
--
ALTER TABLE `tickets_hotelprices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_hotelprices_hotel_id_f508472e` (`hotel_id`);

--
-- Indexes for table `tickets_hotelrooms`
--
ALTER TABLE `tickets_hotelrooms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_hotelrooms_hotel_id_9d09205a` (`hotel_id`);

--
-- Indexes for table `tickets_hotels`
--
ALTER TABLE `tickets_hotels`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_hotels_organization_id_885559b1` (`organization_id`),
  ADD KEY `tickets_hotels_city_id_97f0e5b7` (`city_id`);

--
-- Indexes for table `tickets_roomdetails`
--
ALTER TABLE `tickets_roomdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_roomdetails_room_id_4e7a7a56` (`room_id`);

--
-- Indexes for table `tickets_tickerstopoverdetails`
--
ALTER TABLE `tickets_tickerstopoverdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_tickerstopoverdetails_stopover_city_id_d4818911` (`stopover_city_id`),
  ADD KEY `tickets_tickerstopoverdetails_ticket_id_84687505` (`ticket_id`);

--
-- Indexes for table `tickets_ticket`
--
ALTER TABLE `tickets_ticket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_ticket_airline_id_c2449ee2` (`airline_id`),
  ADD KEY `tickets_ticket_organization_id_7128da48` (`organization_id`);

--
-- Indexes for table `tickets_tickettripdetails`
--
ALTER TABLE `tickets_tickettripdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tickets_tickettripdetails_arrival_city_id_e626ab3f` (`arrival_city_id`),
  ADD KEY `tickets_tickettripdetails_departure_city_id_122d0c29` (`departure_city_id`),
  ADD KEY `tickets_tickettripdetails_ticket_id_a3de7627` (`ticket_id`);

--
-- Indexes for table `users_groupextension`
--
ALTER TABLE `users_groupextension`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `group_id` (`group_id`),
  ADD KEY `users_groupextension_organization_id_179b335c` (`organization_id`);

--
-- Indexes for table `users_permissionextension`
--
ALTER TABLE `users_permissionextension`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `permission_id` (`permission_id`);

--
-- Indexes for table `users_userprofile`
--
ALTER TABLE `users_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `vehicle_type`
--
ALTER TABLE `vehicle_type`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehicle_type_big_sector_id_ab77665a` (`big_sector_id`),
  ADD KEY `vehicle_type_organization_id_bd19ec87` (`organization_id`),
  ADD KEY `vehicle_type_small_sector_id_9b82becf` (`small_sector_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=303;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `big_sector`
--
ALTER TABLE `big_sector`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `big_sector_small_sectors`
--
ALTER TABLE `big_sector_small_sectors`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `booking_allowedreseller`
--
ALTER TABLE `booking_allowedreseller`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking_allowedreseller_reseller_companies`
--
ALTER TABLE `booking_allowedreseller_reseller_companies`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking_bank`
--
ALTER TABLE `booking_bank`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `booking_bankaccount`
--
ALTER TABLE `booking_bankaccount`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking_booking`
--
ALTER TABLE `booking_booking`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT for table `booking_bookinghoteldetails`
--
ALTER TABLE `booking_bookinghoteldetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `booking_bookingpersoncontactdetails`
--
ALTER TABLE `booking_bookingpersoncontactdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `booking_bookingpersondetail`
--
ALTER TABLE `booking_bookingpersondetail`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `booking_bookingpersonfooddetails`
--
ALTER TABLE `booking_bookingpersonfooddetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking_bookingpersonziyaratdetails`
--
ALTER TABLE `booking_bookingpersonziyaratdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking_bookingticketdetails`
--
ALTER TABLE `booking_bookingticketdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `booking_bookingticketstopoverdetails`
--
ALTER TABLE `booking_bookingticketstopoverdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `booking_bookingtickettickettripdetails`
--
ALTER TABLE `booking_bookingtickettickettripdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `booking_bookingtransportdetails`
--
ALTER TABLE `booking_bookingtransportdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `booking_bookingtransportsector`
--
ALTER TABLE `booking_bookingtransportsector`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `booking_booking_internals`
--
ALTER TABLE `booking_booking_internals`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `booking_discount`
--
ALTER TABLE `booking_discount`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `booking_discountgroup`
--
ALTER TABLE `booking_discountgroup`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `booking_internalnote`
--
ALTER TABLE `booking_internalnote`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `booking_markup`
--
ALTER TABLE `booking_markup`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking_organizationlink`
--
ALTER TABLE `booking_organizationlink`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `booking_payment`
--
ALTER TABLE `booking_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=124;

--
-- AUTO_INCREMENT for table `organization_agency`
--
ALTER TABLE `organization_agency`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `organization_agencycontact`
--
ALTER TABLE `organization_agencycontact`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `organization_agencyfiles`
--
ALTER TABLE `organization_agencyfiles`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `organization_agency_user`
--
ALTER TABLE `organization_agency_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `organization_branch`
--
ALTER TABLE `organization_branch`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `organization_branch_user`
--
ALTER TABLE `organization_branch_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `organization_organization`
--
ALTER TABLE `organization_organization`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `organization_organization_user`
--
ALTER TABLE `organization_organization_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `packages_airlines`
--
ALTER TABLE `packages_airlines`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `packages_bookingexpiry`
--
ALTER TABLE `packages_bookingexpiry`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `packages_city`
--
ALTER TABLE `packages_city`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `packages_customumrahfooddetails`
--
ALTER TABLE `packages_customumrahfooddetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `packages_customumrahpackage`
--
ALTER TABLE `packages_customumrahpackage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `packages_customumrahpackagehoteldetails`
--
ALTER TABLE `packages_customumrahpackagehoteldetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `packages_customumrahpackageticketdetails`
--
ALTER TABLE `packages_customumrahpackageticketdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `packages_customumrahpackagetransportdetails`
--
ALTER TABLE `packages_customumrahpackagetransportdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `packages_customumrahziaratdetails`
--
ALTER TABLE `packages_customumrahziaratdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `packages_foodprice`
--
ALTER TABLE `packages_foodprice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `packages_onlyvisaprice`
--
ALTER TABLE `packages_onlyvisaprice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `packages_riyalrate`
--
ALTER TABLE `packages_riyalrate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `packages_setvisatype`
--
ALTER TABLE `packages_setvisatype`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `packages_shirka`
--
ALTER TABLE `packages_shirka`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `packages_transportsectorprice`
--
ALTER TABLE `packages_transportsectorprice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `packages_umrahpackage`
--
ALTER TABLE `packages_umrahpackage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `packages_umrahpackagediscountdetails`
--
ALTER TABLE `packages_umrahpackagediscountdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `packages_umrahpackagehoteldetails`
--
ALTER TABLE `packages_umrahpackagehoteldetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `packages_umrahpackageticketdetails`
--
ALTER TABLE `packages_umrahpackageticketdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `packages_umrahpackagetransportdetails`
--
ALTER TABLE `packages_umrahpackagetransportdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `packages_umrahvisaprice`
--
ALTER TABLE `packages_umrahvisaprice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `packages_umrahvisapricetwo`
--
ALTER TABLE `packages_umrahvisapricetwo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `packages_umrahvisapricetwohotel`
--
ALTER TABLE `packages_umrahvisapricetwohotel`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `packages_umrahvisapricetwo_vehicle_types`
--
ALTER TABLE `packages_umrahvisapricetwo_vehicle_types`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `packages_ziaratprice`
--
ALTER TABLE `packages_ziaratprice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `small_sector`
--
ALTER TABLE `small_sector`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `tickets_hotelcontactdetails`
--
ALTER TABLE `tickets_hotelcontactdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `tickets_hotelprices`
--
ALTER TABLE `tickets_hotelprices`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=149;

--
-- AUTO_INCREMENT for table `tickets_hotelrooms`
--
ALTER TABLE `tickets_hotelrooms`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tickets_hotels`
--
ALTER TABLE `tickets_hotels`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `tickets_roomdetails`
--
ALTER TABLE `tickets_roomdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tickets_tickerstopoverdetails`
--
ALTER TABLE `tickets_tickerstopoverdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `tickets_ticket`
--
ALTER TABLE `tickets_ticket`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `tickets_tickettripdetails`
--
ALTER TABLE `tickets_tickettripdetails`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT for table `users_groupextension`
--
ALTER TABLE `users_groupextension`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `users_permissionextension`
--
ALTER TABLE `users_permissionextension`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users_userprofile`
--
ALTER TABLE `users_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `vehicle_type`
--
ALTER TABLE `vehicle_type`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
