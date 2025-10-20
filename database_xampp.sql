-- ===================================================
-- SQL Import File for Student Management System
-- Tương thích với MySQL 5.7+ (XAMPP)
-- Cập nhật: 2025-10-20 18:58:58
-- ===================================================
--
-- ✅ TẤT CẢ USER ĐÃ CÓ PASSWORD: admin
-- ✅ SAU KHI IMPORT - LOGIN NGAY!
--
-- DANH SÁCH TÀI KHOẢN:
-- 👨‍💼 admin@gmail.com / admin
-- 👨‍🏫 staff1@gmail.com / admin
-- 👨‍🏫 staff2@gmail.com / admin
-- 👨‍🏫 staff3@gmail.com / admin
-- 👨‍🏫 staff4@gmail.com / admin
-- 👨‍🎓 student1@gmail.com / admin
-- 👨‍🎓 student2@gmail.com / admin
--
-- CÁC CẬP NHẬT MỚI:
-- ✅ Bảng student_management_app_subjects:
--    - Thêm cột subject_code VARCHAR(50) - Mã môn học
--    - Thêm cột description TEXT - Mô tả chi tiết môn học
--    - Thêm cột description_file VARCHAR(100) - File PDF mô tả
-- ✅ 19 môn học đã được cập nhật mã môn (MH_1 đến AN_NINH)
-- ✅ Hệ thống chấm điểm mới:
--    - Giảng viên nhập 0-100
--    - Tự động × 0.4 cho BT, × 0.6 cho Thi
--    - Lưu trong subject_assignment_marks và subject_exam_marks
--
-- ===================================================

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


-- Bảng: auth_group
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Bảng: auth_group_permissions
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Bảng: auth_permission
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b_fk_django_co` (`content_type_id`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `auth_permission`
LOCK TABLES `auth_permission` WRITE;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_customuser'),
(22, 'Can change user', 6, 'change_customuser'),
(23, 'Can delete user', 6, 'delete_customuser'),
(24, 'Can view user', 6, 'view_customuser'),
(25, 'Can add attendance', 7, 'add_attendance'),
(26, 'Can change attendance', 7, 'change_attendance'),
(27, 'Can delete attendance', 7, 'delete_attendance'),
(28, 'Can view attendance', 7, 'view_attendance'),
(29, 'Can add courses', 8, 'add_courses'),
(30, 'Can change courses', 8, 'change_courses'),
(31, 'Can delete courses', 8, 'delete_courses'),
(32, 'Can view courses', 8, 'view_courses'),
(33, 'Can add session year model', 9, 'add_sessionyearmodel'),
(34, 'Can change session year model', 9, 'change_sessionyearmodel'),
(35, 'Can delete session year model', 9, 'delete_sessionyearmodel'),
(36, 'Can view session year model', 9, 'view_sessionyearmodel'),
(37, 'Can add subjects', 10, 'add_subjects'),
(38, 'Can change subjects', 10, 'change_subjects'),
(39, 'Can delete subjects', 10, 'delete_subjects'),
(40, 'Can view subjects', 10, 'view_subjects'),
(41, 'Can add students', 11, 'add_students'),
(42, 'Can change students', 11, 'change_students'),
(43, 'Can delete students', 11, 'delete_students'),
(44, 'Can view students', 11, 'view_students'),
(45, 'Can add staffs', 12, 'add_staffs'),
(46, 'Can change staffs', 12, 'change_staffs'),
(47, 'Can delete staffs', 12, 'delete_staffs'),
(48, 'Can view staffs', 12, 'view_staffs'),
(49, 'Can add notification student', 13, 'add_notificationstudent'),
(50, 'Can change notification student', 13, 'change_notificationstudent'),
(51, 'Can delete notification student', 13, 'delete_notificationstudent'),
(52, 'Can view notification student', 13, 'view_notificationstudent'),
(53, 'Can add notification staffs', 14, 'add_notificationstaffs'),
(54, 'Can change notification staffs', 14, 'change_notificationstaffs'),
(55, 'Can delete notification staffs', 14, 'delete_notificationstaffs'),
(56, 'Can view notification staffs', 14, 'view_notificationstaffs'),
(57, 'Can add leave report student', 15, 'add_leavereportstudent'),
(58, 'Can change leave report student', 15, 'change_leavereportstudent'),
(59, 'Can delete leave report student', 15, 'delete_leavereportstudent'),
(60, 'Can view leave report student', 15, 'view_leavereportstudent'),
(61, 'Can add leave report staff', 16, 'add_leavereportstaff'),
(62, 'Can change leave report staff', 16, 'change_leavereportstaff'),
(63, 'Can delete leave report staff', 16, 'delete_leavereportstaff'),
(64, 'Can view leave report staff', 16, 'view_leavereportstaff'),
(65, 'Can add feed back student', 17, 'add_feedbackstudent'),
(66, 'Can change feed back student', 17, 'change_feedbackstudent'),
(67, 'Can delete feed back student', 17, 'delete_feedbackstudent'),
(68, 'Can view feed back student', 17, 'view_feedbackstudent'),
(69, 'Can add feed back staffs', 18, 'add_feedbackstaffs'),
(70, 'Can change feed back staffs', 18, 'change_feedbackstaffs'),
(71, 'Can delete feed back staffs', 18, 'delete_feedbackstaffs'),
(72, 'Can view feed back staffs', 18, 'view_feedbackstaffs'),
(73, 'Can add attendance report', 19, 'add_attendancereport'),
(74, 'Can change attendance report', 19, 'change_attendancereport'),
(75, 'Can delete attendance report', 19, 'delete_attendancereport'),
(76, 'Can view attendance report', 19, 'view_attendancereport'),
(77, 'Can add admin hod', 20, 'add_adminhod'),
(78, 'Can change admin hod', 20, 'change_adminhod'),
(79, 'Can delete admin hod', 20, 'delete_adminhod'),
(80, 'Can view admin hod', 20, 'view_adminhod'),
(81, 'Can add student result', 21, 'add_studentresult'),
(82, 'Can change student result', 21, 'change_studentresult'),
(83, 'Can delete student result', 21, 'delete_studentresult'),
(84, 'Can view student result', 21, 'view_studentresult'),
(85, 'Can add online class room', 22, 'add_onlineclassroom'),
(86, 'Can change online class room', 22, 'change_onlineclassroom'),
(87, 'Can delete online class room', 22, 'delete_onlineclassroom'),
(88, 'Can view online class room', 22, 'view_onlineclassroom'),
(89, 'Can add schedule', 23, 'add_schedule'),
(90, 'Can change schedule', 23, 'change_schedule'),
(91, 'Can delete schedule', 23, 'delete_schedule'),
(92, 'Can view schedule', 23, 'view_schedule'),
(93, 'Can add student enrollment', 24, 'add_studentenrollment'),
(94, 'Can change student enrollment', 24, 'change_studentenrollment'),
(95, 'Can delete student enrollment', 24, 'delete_studentenrollment'),
(96, 'Can view student enrollment', 24, 'view_studentenrollment');
UNLOCK TABLES;


-- Bảng: django_admin_log
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_student_m` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_student_m` FOREIGN KEY (`user_id`) REFERENCES `student_management_app_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Bảng: django_content_type
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `django_content_type`
LOCK TABLES `django_content_type` WRITE;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(20, 'student_management_app', 'adminhod'),
(7, 'student_management_app', 'attendance'),
(19, 'student_management_app', 'attendancereport'),
(8, 'student_management_app', 'courses'),
(6, 'student_management_app', 'customuser'),
(18, 'student_management_app', 'feedbackstaffs'),
(17, 'student_management_app', 'feedbackstudent'),
(16, 'student_management_app', 'leavereportstaff'),
(15, 'student_management_app', 'leavereportstudent'),
(14, 'student_management_app', 'notificationstaffs'),
(13, 'student_management_app', 'notificationstudent'),
(22, 'student_management_app', 'onlineclassroom'),
(23, 'student_management_app', 'schedule'),
(9, 'student_management_app', 'sessionyearmodel'),
(12, 'student_management_app', 'staffs'),
(24, 'student_management_app', 'studentenrollment'),
(21, 'student_management_app', 'studentresult'),
(11, 'student_management_app', 'students'),
(10, 'student_management_app', 'subjects');
UNLOCK TABLES;


-- Bảng: django_migrations
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `django_migrations`
LOCK TABLES `django_migrations` WRITE;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-04-12 08:09:49.732772'),
(2, 'contenttypes', '0002_remove_content_type_name', '2020-04-12 08:09:49.916310'),
(3, 'auth', '0001_initial', '2020-04-12 08:09:50.001645'),
(4, 'auth', '0002_alter_permission_name_max_length', '2020-04-12 08:09:50.266520'),
(5, 'auth', '0003_alter_user_email_max_length', '2020-04-12 08:09:50.277458'),
(6, 'auth', '0004_alter_user_username_opts', '2020-04-12 08:09:50.292747'),
(7, 'auth', '0005_alter_user_last_login_null', '2020-04-12 08:09:50.300324'),
(8, 'auth', '0006_require_contenttypes_0002', '2020-04-12 08:09:50.305224'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2020-04-12 08:09:50.313290'),
(10, 'auth', '0008_alter_user_username_max_length', '2020-04-12 08:09:50.322160'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2020-04-12 08:09:50.333818'),
(12, 'auth', '0010_alter_group_name_max_length', '2020-04-12 08:09:50.355384'),
(13, 'auth', '0011_update_proxy_permissions', '2020-04-12 08:09:50.367427'),
(14, 'student_management_app', '0001_initial', '2020-04-12 08:09:51.816963'),
(15, 'admin', '0001_initial', '2020-04-12 08:09:54.256426'),
(16, 'admin', '0002_logentry_remove_auto_add', '2020-04-12 08:09:54.391340'),
(17, 'admin', '0003_logentry_add_action_flag_choices', '2020-04-12 08:09:54.408406'),
(18, 'sessions', '0001_initial', '2020-04-12 08:09:54.459617'),
(19, 'student_management_app', '0002_auto_20200502_1839', '2020-05-02 13:09:56.696264'),
(20, 'student_management_app', '0002_auto_20200507_1430', '2020-05-07 09:00:39.284817'),
(21, 'student_management_app', '0003_auto_20200510_1919', '2020-05-10 13:49:34.938810'),
(22, 'student_management_app', '0004_auto_20200523_1321', '2020-05-23 07:51:13.682476'),
(23, 'auth', '0012_alter_user_first_name_max_length', '2025-10-20 09:18:45.719762'),
(24, 'student_management_app', '0002_onlineclassroom', '2025-10-20 09:18:45.906300'),
(25, 'student_management_app', '0003_alter_customuser_first_name', '2025-10-20 09:18:45.922149'),
(26, 'student_management_app', '0004_subjects_credit_hours_subjects_fee_per_credit_and_more', '2025-10-20 09:18:46.246523'),
(27, 'student_management_app', '0005_alter_subjects_fee_per_credit', '2025-10-20 09:49:48.987222'),
(28, 'student_management_app', '0006_subjects_description_subjects_description_file_and_more', '2025-10-20 11:47:10.775149');
UNLOCK TABLES;


-- Bảng: django_session
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `django_session`
LOCK TABLES `django_session` WRITE;
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('4uafupyvuwgg8hsxkrbyvr6dr5flanz0', 'MTkxMzk4ODg5ZjE2ZmJmNzFiYzU4ZDYzYTZmNjU5NzE1ZTY1ZGFkODp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic3R1ZGVudF9tYW5hZ2VtZW50X2FwcC5FbWFpbEJhY2tFbmQuRW1haWxCYWNrRW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWI2YTk5ZjEwMzM0MDdjYmE0NmZjZGZlZDEyZGM5NzhhOTM3Y2JmMyJ9', '2020-06-09 08:15:00.200912'),
('m8eqtizu2bo12n6nayfu1vi7zh7tbfhz', '.eJxVjMEOgyAQRP-Fc9PgLiL02MTvIAu7VNNKTMFT03-v3uptZt7kfVSgrU1hq_IOM6ubAnX53yKlp5QD1LaxlBYWKvSQ5Yi0rtdxofl1319j4VM5eyaq0y7pEHyfGI1DcboDk7Ud0IrFrmeA5DGzyZh1dGQGspR8jjh4ABdJZ1bfH5dGOi4:1vAo0n:NGdyEpX4AuKyp6mepq-tFpP0js7-zndoqkAu789K8gM', '2025-11-03 11:25:13.866969'),
('z25qqlq023k6i2veud817qctrlxk63fn', 'MTkxMzk4ODg5ZjE2ZmJmNzFiYzU4ZDYzYTZmNjU5NzE1ZTY1ZGFkODp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic3R1ZGVudF9tYW5hZ2VtZW50X2FwcC5FbWFpbEJhY2tFbmQuRW1haWxCYWNrRW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWI2YTk5ZjEwMzM0MDdjYmE0NmZjZGZlZDEyZGM5NzhhOTM3Y2JmMyJ9', '2020-05-24 14:09:45.204277');
UNLOCK TABLES;


-- Bảng: student_management_app_adminhod
DROP TABLE IF EXISTS `student_management_app_adminhod`;
CREATE TABLE `student_management_app_adminhod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `admin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_id` (`admin_id`),
  CONSTRAINT `student_management_a_admin_id_2d75304f_fk_student_m` FOREIGN KEY (`admin_id`) REFERENCES `student_management_app_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_adminhod`
LOCK TABLES `student_management_app_adminhod` WRITE;
INSERT INTO `student_management_app_adminhod` (`id`, `created_at`, `updated_at`, `admin_id`) VALUES
(1, '2020-04-12 08:16:07.103523', '2020-04-12 08:16:07.103523', 1),
(2, '2025-10-20 09:22:58.742662', '2025-10-20 09:22:58.742685', 16);
UNLOCK TABLES;


-- Bảng: student_management_app_attendance
DROP TABLE IF EXISTS `student_management_app_attendance`;
CREATE TABLE `student_management_app_attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attendance_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `session_year_id_id` int(11) NOT NULL,
  `subject_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_session_year_id_id_0d30545d_fk_student_m` (`session_year_id_id`),
  KEY `student_management_a_subject_id_id_9ae82fd0_fk_student_m` (`subject_id_id`),
  CONSTRAINT `student_management_a_session_year_id_id_0d30545d_fk_student_m` FOREIGN KEY (`session_year_id_id`) REFERENCES `student_management_app_sessionyearmodel` (`id`),
  CONSTRAINT `student_management_a_subject_id_id_9ae82fd0_fk_student_m` FOREIGN KEY (`subject_id_id`) REFERENCES `student_management_app_subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_attendance`
LOCK TABLES `student_management_app_attendance` WRITE;
INSERT INTO `student_management_app_attendance` (`id`, `attendance_date`, `created_at`, `updated_at`, `session_year_id_id`, `subject_id_id`) VALUES
(4, '2020-04-12', '2020-04-12 11:49:25.282944', '2020-04-12 11:49:25.282944', 1, 1),
(5, '2020-04-12', '2020-04-12 11:49:51.034169', '2020-04-12 11:49:51.034169', 1, 2),
(6, '2020-05-07', '2020-05-07 14:19:12.327810', '2020-05-07 14:19:12.327810', 1, 1),
(7, '2020-05-07', '2020-05-07 14:19:25.800828', '2020-05-07 14:19:25.800828', 1, 1),
(8, '2020-05-07', '2020-05-07 14:19:45.100649', '2020-05-07 14:19:45.100649', 1, 1),
(9, '2020-05-07', '2020-05-07 14:28:08.882707', '2020-05-07 14:28:08.882707', 2, 2),
(10, '2020-05-07', '2020-05-07 08:58:38.167460', '2020-05-07 08:58:38.168149', 2, 2),
(11, '2020-05-07', '2020-05-07 08:59:15.875971', '2020-05-07 08:59:15.875971', 1, 1),
(12, '2020-05-07', '2020-05-07 08:59:15.887974', '2020-05-07 08:59:15.887974', 1, 1),
(13, '2020-05-10', '2020-05-07 09:00:59.318549', '2020-05-07 09:00:59.318549', 1, 1),
(14, '2020-05-17', '2020-05-07 14:31:31.654667', '2020-05-07 14:31:31.654667', 1, 1),
(15, '2020-05-10', '2020-05-07 14:39:11.790480', '2020-05-07 14:39:11.790480', 1, 2),
(16, '2020-05-15', '2020-05-10 14:10:11.214771', '2020-05-10 14:10:11.214771', 1, 1);
UNLOCK TABLES;


-- Bảng: student_management_app_attendancereport
DROP TABLE IF EXISTS `student_management_app_attendancereport`;
CREATE TABLE `student_management_app_attendancereport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `attendance_id_id` int(11) NOT NULL,
  `student_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_attendance_id_id_f765f2a1_fk_student_m` (`attendance_id_id`),
  KEY `student_management_a_student_id_id_5a58ceea_fk_student_m` (`student_id_id`),
  CONSTRAINT `student_management_a_attendance_id_id_f765f2a1_fk_student_m` FOREIGN KEY (`attendance_id_id`) REFERENCES `student_management_app_attendance` (`id`),
  CONSTRAINT `student_management_a_student_id_id_5a58ceea_fk_student_m` FOREIGN KEY (`student_id_id`) REFERENCES `student_management_app_students` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_attendancereport`
LOCK TABLES `student_management_app_attendancereport` WRITE;
INSERT INTO `student_management_app_attendancereport` (`id`, `status`, `created_at`, `updated_at`, `attendance_id_id`, `student_id_id`) VALUES
(3, 1, '2020-04-12 11:49:25.305883', '2020-04-12 11:49:25.305883', 4, 2),
(4, 0, '2020-04-12 11:49:25.309871', '2020-04-12 11:49:25.309871', 4, 3),
(5, 1, '2020-04-12 11:49:51.057109', '2020-04-12 11:49:51.057109', 5, 2),
(6, 0, '2020-04-12 11:49:51.062096', '2020-04-12 11:49:51.062096', 5, 3),
(7, 1, '2020-05-07 14:19:12.445501', '2020-05-07 14:19:12.445501', 6, 2),
(8, 1, '2020-05-07 14:19:12.470390', '2020-05-07 14:19:12.470390', 6, 3),
(9, 1, '2020-05-07 14:19:25.923632', '2020-05-07 14:19:25.923632', 7, 2),
(10, 0, '2020-05-07 14:19:25.930384', '2020-05-07 14:19:25.930384', 7, 3),
(11, 1, '2020-05-07 14:19:45.110865', '2020-05-07 14:19:45.110865', 8, 2),
(12, 0, '2020-05-07 14:19:45.118596', '2020-05-07 14:19:45.118596', 8, 3),
(13, 1, '2020-05-07 08:59:16.235068', '2020-05-07 08:59:16.235068', 11, 2),
(14, 1, '2020-05-07 08:59:16.237053', '2020-05-07 08:59:16.237053', 12, 2),
(15, 1, '2020-05-07 08:59:16.253009', '2020-05-07 08:59:16.253009', 11, 3),
(16, 1, '2020-05-07 08:59:16.256287', '2020-05-07 08:59:16.256287', 12, 3),
(17, 1, '2020-05-07 09:00:59.347431', '2020-05-07 09:00:59.347431', 13, 2),
(18, 1, '2020-05-07 09:00:59.355410', '2020-05-07 09:00:59.355410', 13, 3),
(19, 1, '2020-05-07 14:31:31.667624', '2020-05-07 14:31:31.667624', 14, 2),
(20, 1, '2020-05-07 14:31:32.003679', '2020-05-07 14:31:32.003679', 14, 3),
(21, 1, '2020-05-07 14:39:12.115953', '2020-05-07 14:39:12.115953', 15, 2),
(22, 0, '2020-05-07 14:39:12.120941', '2020-05-07 14:39:12.120941', 15, 3),
(23, 1, '2020-05-10 14:10:11.238705', '2020-05-10 14:10:11.238705', 16, 2),
(24, 1, '2020-05-10 14:10:11.242699', '2020-05-10 14:10:11.242699', 16, 3);
UNLOCK TABLES;


-- Bảng: student_management_app_courses
DROP TABLE IF EXISTS `student_management_app_courses`;
CREATE TABLE `student_management_app_courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_courses`
LOCK TABLES `student_management_app_courses` WRITE;
INSERT INTO `student_management_app_courses` (`id`, `course_name`, `created_at`, `updated_at`) VALUES
(1, 'Cử nhân Tin học Ứng dụng', '2020-04-12 08:37:10.306437', '2020-04-12 08:37:10.306437'),
(2, 'Cử nhân Quản trị Kinh doanh', '2020-04-12 08:37:14.880271', '2020-04-12 08:37:14.880271'),
(3, 'Thạc sĩ Quản trị Kinh doanh', '2020-04-12 08:37:18.160619', '2020-04-12 08:37:18.160619'),
(4, 'Thạc sĩ Tin học Ứng dụng', '2020-04-12 08:37:21.825105', '2020-04-12 08:37:21.825105'),
(5, 'Khoa học Máy tính', '2025-10-20 09:22:02.301886', '2025-10-20 09:22:02.301924'),
(6, 'Công nghệ Thông tin', '2025-10-20 09:46:01.907647', '2025-10-20 09:46:01.907682'),
(7, 'Kỹ thuật Phần mềm', '2025-10-20 09:46:01.913478', '2025-10-20 09:46:01.913496'),
(8, 'Kỹ thuật Điện - Điện tử', '2025-10-20 09:46:01.916029', '2025-10-20 09:46:01.916047'),
(9, 'Kỹ thuật Cơ khí', '2025-10-20 09:46:01.918714', '2025-10-20 09:46:01.918728'),
(10, 'Kỹ thuật Xây dựng', '2025-10-20 09:46:01.921525', '2025-10-20 09:46:01.921545'),
(11, 'Kiến trúc', '2025-10-20 09:46:01.924302', '2025-10-20 09:46:01.924321'),
(12, 'Kế toán', '2025-10-20 09:46:01.927144', '2025-10-20 09:46:01.927163'),
(13, 'Tài chính - Ngân hàng', '2025-10-20 09:46:01.930447', '2025-10-20 09:46:01.930466'),
(14, 'Marketing', '2025-10-20 09:46:01.932848', '2025-10-20 09:46:01.932866'),
(15, 'Kinh tế học', '2025-10-20 09:46:01.935901', '2025-10-20 09:46:01.935920'),
(16, 'Ngôn ngữ Anh', '2025-10-20 09:46:01.939008', '2025-10-20 09:46:01.939026'),
(17, 'Luật', '2025-10-20 09:46:01.942200', '2025-10-20 09:46:01.942223'),
(18, 'Toán học', '2025-10-20 09:46:01.945065', '2025-10-20 09:46:01.945083');
UNLOCK TABLES;


-- Bảng: student_management_app_customuser
DROP TABLE IF EXISTS `student_management_app_customuser`;
CREATE TABLE `student_management_app_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_type` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_customuser`
LOCK TABLES `student_management_app_customuser` WRITE;
INSERT INTO `student_management_app_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `user_type`) VALUES
(1, 'pbkdf2_sha256$600000$qZFNwj4k7F2rkedyDLoXAL$6GXJVwsYwMcPjYo6PrfHJpx2kTeJikGqZYFUkG8nKV0=', '2020-05-25 17:03:59.941387', 1, 'admin', 'Admin First 1', 'Admin Last 2', 'admin@gmail.com', 1, 1, '2020-04-12 08:16:06.881413', '1'),
(2, 'pbkdf2_sha256$600000$5oQvga9MQ96tTUsGrzZxeE$vTWhNJEaGjuJy/BLx9MEAOU+gcHJNmcaRs1e1F+zasY=', '2025-10-20 11:25:13.861991', 0, 'staff1', 'Staff First 1 1', 'Staff One Address 3 1', 'staff1@gmail.com', 0, 1, '2020-04-12 08:38:05.596253', '2'),
(3, 'pbkdf2_sha256$600000$bOiWGDBOs9KU1UMimsDdLQ$pTMSt1//Ql0avbCjkZRyYk/9XtXDJe8ND2bldJ7s9mc=', '2020-05-07 10:20:47.673389', 0, 'staff2', 'Staff', 'Two', 'staff2@gmail.com', 0, 1, '2020-04-12 08:38:29.881934', '2'),
(4, 'pbkdf2_sha256$600000$6M66JtSCKgy5w7ODbhJ2Uu$NzyoA7/C4TqeVF8kvHVA7T6Rx0qpD5BDJtv9yxpco58=', NULL, 0, 'staff3', 'Staff', 'Three', 'staff3@gmail.com', 0, 1, '2020-04-12 08:38:51.139627', '2'),
(5, 'pbkdf2_sha256$600000$a9EfTZs06mSxVzHdwwV0cD$QX+GlrSxylntkflXra7Rjii7NL9jXzZ3q/tgpmOy1IQ=', NULL, 0, 'staff4', 'Staff', 'Four', 'staff4@gmail.com', 0, 1, '2020-04-12 08:39:16.924296', '2'),
(13, 'pbkdf2_sha256$1000000$awVNp4ddznXHp7Jw1Wlb4z$A6tfj0shrlsFa8LlWXMltnN5BvOOnMoOsj94dZQ1ZiU=', '2020-05-05 07:53:44.763359', 0, 'student1', 'Student', 'One', 'student1@gmail.com', 0, 1, '2020-04-12 08:59:08.372628', '3'),
(14, 'pbkdf2_sha256$1000000$uBdpyZEKpunOXtuAKuTWEd$jXVVTL1R7gfHwH2+q9czLBmdp55XKzPKs0XpC/AwhGs=', '2020-05-26 08:14:12.403741', 0, 'student2', 'student First', 'Two Last', 'student2@gmail.com', 0, 1, '2020-04-12 09:00:14.371150', '3'),
(16, 'pbkdf2_sha256$600000$SX8sVij2CJA8hQo8ML5r2g$4lhBbDgmsdxdOxdsOIPCoeWedvqIynMaxmeXp7Ua1B4=', '2025-10-20 09:42:47.137218', 1, 'admin_test', 'Admin', 'Test', 'admin_test@gmail.com', 1, 1, '2025-10-20 09:22:58.485498', '1'),
(17, 'pbkdf2_sha256$600000$bYPi2YCylGwVfCw9WTP7Gg$V+vunNX5w5dDjiUG+/8uJy7vb2owTQk0zaseI35k2sA=', '2025-10-20 09:25:01.410642', 0, 'lecturer_test', 'Lecturer', 'Test', 'lecturer_test@gmail.com', 0, 1, '2025-10-20 09:22:58.746213', '2'),
(18, 'pbkdf2_sha256$600000$BHFwIGi2q9Ttze7elLE6pN$M+k2LlsYry92i9ToY8Wxivet72z8UGzW/4nIB1lbfgM=', '2025-10-20 09:26:09.956157', 0, 'student_test', 'Student', 'Test', 'student_test@gmail.com', 0, 1, '2025-10-20 09:22:59.016949', '3'),
(19, 'pbkdf2_sha256$600000$viauaWMYxkJKO18dz3VITB$BDvC+ucNdwB2ADk4NiU1jwmEMNqpXSUYYtSN+N64r5Q=', '2025-10-20 10:29:42.627616', 0, 'student_01', 'Hoàng Hoàng', 'Hoa', 'student01@example.com', 0, 1, '2025-10-20 10:04:24.153935', '3'),
(20, 'pbkdf2_sha256$600000$diPTBzb7BQIei1XugIgrVb$+EU/3tqenBWMRSW2K6r2rWe639lKx0wi+HujBW6fosk=', NULL, 0, 'student_02', 'Vũ Hữu', 'Xuân', 'student02@example.com', 0, 1, '2025-10-20 10:04:24.413740', '3'),
(21, 'pbkdf2_sha256$600000$auTspLrupCm1flhpWpocQV$04biAVhq0QgNjOmovfnx8xyAX7tCFk+N1TXm+aMExLw=', NULL, 0, 'student_03', 'Hồ Hồng', 'Quân', 'student03@example.com', 0, 1, '2025-10-20 10:04:24.669931', '3'),
(22, 'pbkdf2_sha256$600000$Yg7KUgIWxF0njm8rRnuLFl$UxX2fVwfwDZk/jF5hQm2fKNTGtZng/mvLoex5fhcRTs=', NULL, 0, 'student_04', 'Đỗ Quốc', 'Chi', 'student04@example.com', 0, 1, '2025-10-20 10:04:24.927174', '3'),
(23, 'pbkdf2_sha256$600000$wbxN4ou6oVZFpu6MyB6sQr$ddkxBPv7b773LtTGVkw1jeTChsDyCddg9Xx2Zzc6wyI=', NULL, 0, 'student_05', 'Phan Khánh', 'Nhung', 'student05@example.com', 0, 1, '2025-10-20 10:04:25.185963', '3'),
(24, 'pbkdf2_sha256$600000$8qbk7zB70p0zZ0sx4yUjiR$7AKyWqBPf6b97wWjOUiXVYnJrZkxr7Oax8tDUg3eosc=', NULL, 0, 'student_06', 'Đỗ Hồng', 'Tú', 'student06@example.com', 0, 1, '2025-10-20 10:04:25.455828', '3'),
(25, 'pbkdf2_sha256$600000$5J6CNBSJCE883Kbio0eHTI$20f7htPHs1f6nPGcCfmGrOYodiHAyyefOGgp8gVx9iA=', NULL, 0, 'student_07', 'Hồ Văn', 'Bảo', 'student07@example.com', 0, 1, '2025-10-20 10:04:25.713227', '3'),
(26, 'pbkdf2_sha256$600000$Ey2AU1BNOKW15EK26LjDT9$YS5oakSfeqX5C5RXy66iasrrFFt4or0JXQtZnjqQdBQ=', NULL, 0, 'student_08', 'Hoàng Khánh', 'Xuân', 'student08@example.com', 0, 1, '2025-10-20 10:04:25.970490', '3'),
(27, 'pbkdf2_sha256$600000$EXLWYcFfEdQt9zNyhVL1bv$NN76aZI+MTCnlyHwuyULlDe6VTREpjs+5DPSGD2q/lw=', NULL, 0, 'student_09', 'Vũ Thanh', 'Hoa', 'student09@example.com', 0, 1, '2025-10-20 10:04:26.220476', '3'),
(28, 'pbkdf2_sha256$600000$MXA3Qd8ITU7X8sHicUnT6c$4Otm+B3GahW2GbeekI5mtq1+v6ZMMksMATqAildqz2k=', NULL, 0, 'student_10', 'Hồ Quốc', 'Hằng', 'student10@example.com', 0, 1, '2025-10-20 10:04:26.471851', '3'),
(29, 'pbkdf2_sha256$600000$j5RtZB4OQJVmHaoKj4Ecxk$KfujqZjGS5HGObYyUUHasV2siQm/cxGHukIHuA8rjdM=', NULL, 0, 'student_14', 'Phan Như', 'Uyên', 'student14@example.com', 0, 1, '2025-10-20 10:16:40.268484', '3'),
(30, 'pbkdf2_sha256$600000$yda4PCXdHXWjfk9lpAuTMJ$p6PQOQ3a4tRnqaEQp/fbkAcMh4L3UBvEnis5XFkhi7g=', NULL, 0, 'student_15', 'Trần Thanh', 'Hằng', 'student15@example.com', 0, 1, '2025-10-20 10:16:40.535772', '3'),
(31, 'pbkdf2_sha256$600000$5UumKeCSeWNRSDGcV5xamn$T8iv1WEBImH1YNB89y4NBbrdIXkQ02g0jl/8DE4inpA=', NULL, 0, 'student_16', 'Hoàng Anh', 'Linh', 'student16@example.com', 0, 1, '2025-10-20 10:16:40.788686', '3'),
(32, 'pbkdf2_sha256$600000$BYswdgloWPNsUcOkQ3NuY3$ryTau1MhrA9xZzJyZrfDsPtpBHAG5TEChOP6meSQ9e8=', NULL, 0, 'student_17', 'Võ Như', 'Yến', 'student17@example.com', 0, 1, '2025-10-20 10:16:41.042741', '3'),
(33, 'pbkdf2_sha256$600000$3UUw6WHsnBMeQKvIMsqfvc$Piaja4TSX5NsUx167pfGbYdppukysGye/DPw23Ypp7o=', NULL, 0, 'student_18', 'Võ Bảo', 'Anh', 'student18@example.com', 0, 1, '2025-10-20 10:16:41.330354', '3'),
(34, 'pbkdf2_sha256$600000$rGdbWu9GYtIgvmTc1JXAvA$sOLllT6UNBlGhlTzIcfwRWo6CwUWypfYjO0x2U/pXqY=', NULL, 0, 'student_19', 'Huỳnh Mai', 'Hoa', 'student19@example.com', 0, 1, '2025-10-20 10:16:41.597705', '3'),
(35, 'pbkdf2_sha256$600000$tQPJf9VQFEX6RJflyoHZkl$v2EkiuU3c8Os8Kqj3YZ4QKYzfLgJCqOMnFwvFa6Nlns=', NULL, 0, 'student_20', 'Tô Bảo', 'Oanh', 'student20@example.com', 0, 1, '2025-10-20 10:16:41.849550', '3'),
(36, 'pbkdf2_sha256$600000$Xn9dwhdxoNhRovvXKC8CIu$JRs5V/BI46e92gXFQjMueStnAjFPki7LEKGkryT8aCU=', NULL, 0, 'student_21', 'Lý Đức', 'Cường', 'student21@example.com', 0, 1, '2025-10-20 10:16:42.114250', '3'),
(37, 'pbkdf2_sha256$600000$myHhBtTJA83bUA8gn7Hi6x$Qb26jmL5p9H9eTvcXJLjoNXopz4N/7UdJdSKPCChFNk=', NULL, 0, 'student_22', 'Dương Hoàng', 'Khánh', 'student22@example.com', 0, 1, '2025-10-20 10:16:42.381138', '3'),
(38, 'pbkdf2_sha256$600000$q60JhGOxMHm41m2B4lmB27$HGLnkhphMSA/RpbV6lczV2DJjIPpfb5VUYnu9ILmLP8=', NULL, 0, 'student_23', 'Đinh Tuấn', 'Em', 'student23@example.com', 0, 1, '2025-10-20 10:16:42.642666', '3'),
(39, 'pbkdf2_sha256$600000$eDia7FhirmNrBPcbA3BqAl$GRDJ5kV1MCPxSpBHIno5lNAVZhv95HVLUJbCkusDQbg=', NULL, 0, 'student_24', 'Dương Phương', 'Vân', 'student24@example.com', 0, 1, '2025-10-20 10:16:42.914174', '3'),
(40, 'pbkdf2_sha256$600000$Y4GEduptEp7hJEu1gh5Dp1$z10LL5CvFEGRWqQrVCYpedgHXMsYwepKRFQdGN+HqY8=', NULL, 0, 'student_25', 'Nguyễn Thanh', 'Hà', 'student25@example.com', 0, 1, '2025-10-20 10:20:56.944934', '3'),
(41, 'pbkdf2_sha256$600000$pW3iKZAl0UYFvYfl2zVJhC$hOaMFgSP3FrKq0IfA+gEGZoIZwcoK7r3xTnHNNS5j9o=', NULL, 0, 'student_26', 'Lê Đức', 'Em', 'student26@example.com', 0, 1, '2025-10-20 10:21:24.509533', '3'),
(42, 'pbkdf2_sha256$600000$KVpxAfT3wlr4CAUn5Oli1c$yQTUFgCjhSntbaL70yAzbFR8tLP6nNiAHacfakE81SI=', NULL, 0, 'student_27', 'Lê Đức', 'Dũng', 'student27@example.com', 0, 1, '2025-10-20 10:21:30.633744', '3'),
(43, 'pbkdf2_sha256$600000$L5gRQ1XEp7cRA2yaeAepJk$2bEHxykWU8wj76nfFrOkE1UfQ4drp4uVrCyb4jzeP4I=', NULL, 0, 'student_28', 'Hoàng Thanh', 'Cường', 'student28@example.com', 0, 1, '2025-10-20 10:22:27.638836', '3');
UNLOCK TABLES;


-- Bảng: student_management_app_customuser_groups
DROP TABLE IF EXISTS `student_management_app_customuser_groups`;
CREATE TABLE `student_management_app_customuser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_management_app_c_customuser_id_group_id_d872a780_uniq` (`customuser_id`,`group_id`),
  KEY `student_management_a_group_id_61accfd6_fk_auth_grou` (`group_id`),
  KEY `student_management_a_customuser_id_1e347552_fk_student_m` (`customuser_id`),
  CONSTRAINT `student_management_a_customuser_id_1e347552_fk_student_m` FOREIGN KEY (`customuser_id`) REFERENCES `student_management_app_customuser` (`id`),
  CONSTRAINT `student_management_a_group_id_61accfd6_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Bảng: student_management_app_customuser_user_permissions
DROP TABLE IF EXISTS `student_management_app_customuser_user_permissions`;
CREATE TABLE `student_management_app_customuser_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_management_app_c_customuser_id_permission_af9a6989_uniq` (`customuser_id`,`permission_id`),
  KEY `student_management_a_permission_id_cd344297_fk_auth_perm` (`permission_id`),
  KEY `student_management_a_customuser_id_41a474d7_fk_student_m` (`customuser_id`),
  CONSTRAINT `student_management_a_customuser_id_41a474d7_fk_student_m` FOREIGN KEY (`customuser_id`) REFERENCES `student_management_app_customuser` (`id`),
  CONSTRAINT `student_management_a_permission_id_cd344297_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Bảng: student_management_app_feedbackstaffs
DROP TABLE IF EXISTS `student_management_app_feedbackstaffs`;
CREATE TABLE `student_management_app_feedbackstaffs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` longtext NOT NULL,
  `feedback_reply` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_staff_id_id_6f22a616_fk_student_m` (`staff_id_id`),
  CONSTRAINT `student_management_a_staff_id_id_6f22a616_fk_student_m` FOREIGN KEY (`staff_id_id`) REFERENCES `student_management_app_staffs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_feedbackstaffs`
LOCK TABLES `student_management_app_feedbackstaffs` WRITE;
INSERT INTO `student_management_app_feedbackstaffs` (`id`, `feedback`, `feedback_reply`, `created_at`, `updated_at`, `staff_id_id`) VALUES
(1, 'Testing Feedback Message', 'I will Contact You', '2020-05-02 13:39:42.882248', '2020-05-02 13:39:42.882248', 1),
(2, 'New Testing', 'Thanks', '2020-05-02 13:40:58.015222', '2020-05-02 13:40:58.015222', 1);
UNLOCK TABLES;


-- Bảng: student_management_app_feedbackstudent
DROP TABLE IF EXISTS `student_management_app_feedbackstudent`;
CREATE TABLE `student_management_app_feedbackstudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` longtext NOT NULL,
  `feedback_reply` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_student_id_id_099e23ad_fk_student_m` (`student_id_id`),
  CONSTRAINT `student_management_a_student_id_id_099e23ad_fk_student_m` FOREIGN KEY (`student_id_id`) REFERENCES `student_management_app_students` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_feedbackstudent`
LOCK TABLES `student_management_app_feedbackstudent` WRITE;
INSERT INTO `student_management_app_feedbackstudent` (`id`, `feedback`, `feedback_reply`, `created_at`, `updated_at`, `student_id_id`) VALUES
(1, 'Need to Contact', 'Thanks for Message', '2020-05-15 09:47:31.700892', '2020-05-15 09:47:31.700892', 3),
(2, 'Need to Contact', 'We Will Contact You', '2020-05-15 09:47:31.700892', '2020-05-15 09:47:31.700892', 3);
UNLOCK TABLES;


-- Bảng: student_management_app_leavereportstaff
DROP TABLE IF EXISTS `student_management_app_leavereportstaff`;
CREATE TABLE `student_management_app_leavereportstaff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `leave_date` varchar(255) NOT NULL,
  `leave_message` longtext NOT NULL,
  `leave_status` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_staff_id_id_c7710cd5_fk_student_m` (`staff_id_id`),
  CONSTRAINT `student_management_a_staff_id_id_c7710cd5_fk_student_m` FOREIGN KEY (`staff_id_id`) REFERENCES `student_management_app_staffs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_leavereportstaff`
LOCK TABLES `student_management_app_leavereportstaff` WRITE;
INSERT INTO `student_management_app_leavereportstaff` (`id`, `leave_date`, `leave_message`, `leave_status`, `created_at`, `updated_at`, `staff_id_id`) VALUES
(1, '2020-05-17', 'Borther Marriage', 1, '2020-05-02 13:20:13.981434', '2020-05-02 13:20:13.981434', 1),
(2, '2020-05-24', 'Sister Marriage', 2, '2020-05-02 13:21:20.513330', '2020-05-02 13:21:20.513330', 1),
(3, '2020-05-31', 'Just Leave', 0, '2020-05-02 13:31:45.231819', '2020-05-02 13:31:45.231819', 1);
UNLOCK TABLES;


-- Bảng: student_management_app_leavereportstudent
DROP TABLE IF EXISTS `student_management_app_leavereportstudent`;
CREATE TABLE `student_management_app_leavereportstudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `leave_date` varchar(255) NOT NULL,
  `leave_message` longtext NOT NULL,
  `leave_status` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_student_id_id_9ea5372c_fk_student_m` (`student_id_id`),
  CONSTRAINT `student_management_a_student_id_id_9ea5372c_fk_student_m` FOREIGN KEY (`student_id_id`) REFERENCES `student_management_app_students` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_leavereportstudent`
LOCK TABLES `student_management_app_leavereportstudent` WRITE;
INSERT INTO `student_management_app_leavereportstudent` (`id`, `leave_date`, `leave_message`, `leave_status`, `created_at`, `updated_at`, `student_id_id`) VALUES
(1, '2020-05-16', 'Formal Leave', 1, '2020-05-15 09:46:09.709208', '2020-05-15 09:46:09.709208', 3),
(2, '2020-05-20', 'Leave', 2, '2020-05-15 09:46:20.765721', '2020-05-15 09:46:20.765721', 3),
(3, '2020-05-20', 'Leave', 0, '2020-05-15 09:46:20.765721', '2020-05-15 09:46:20.765721', 3);
UNLOCK TABLES;


-- Bảng: student_management_app_notificationstaffs
DROP TABLE IF EXISTS `student_management_app_notificationstaffs`;
CREATE TABLE `student_management_app_notificationstaffs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_staff_id_id_2d336ab5_fk_student_m` (`staff_id_id`),
  CONSTRAINT `student_management_a_staff_id_id_2d336ab5_fk_student_m` FOREIGN KEY (`staff_id_id`) REFERENCES `student_management_app_staffs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Bảng: student_management_app_notificationstudent
DROP TABLE IF EXISTS `student_management_app_notificationstudent`;
CREATE TABLE `student_management_app_notificationstudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_student_id_id_f8c05ed7_fk_student_m` (`student_id_id`),
  CONSTRAINT `student_management_a_student_id_id_f8c05ed7_fk_student_m` FOREIGN KEY (`student_id_id`) REFERENCES `student_management_app_students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Bảng: student_management_app_onlineclassroom
DROP TABLE IF EXISTS `student_management_app_onlineclassroom`;
CREATE TABLE `student_management_app_onlineclassroom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_name` varchar(255) NOT NULL,
  `room_pwd` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `session_years_id` int(11) NOT NULL,
  `started_by_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_session_years_id_c7d9b709_fk_student_m` (`session_years_id`),
  KEY `student_management_a_started_by_id_8850ac2b_fk_student_m` (`started_by_id`),
  KEY `student_management_a_subject_id_78d7e366_fk_student_m` (`subject_id`),
  CONSTRAINT `student_management_a_session_years_id_c7d9b709_fk_student_m` FOREIGN KEY (`session_years_id`) REFERENCES `student_management_app_sessionyearmodel` (`id`),
  CONSTRAINT `student_management_a_started_by_id_8850ac2b_fk_student_m` FOREIGN KEY (`started_by_id`) REFERENCES `student_management_app_staffs` (`id`),
  CONSTRAINT `student_management_a_subject_id_78d7e366_fk_student_m` FOREIGN KEY (`subject_id`) REFERENCES `student_management_app_subjects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Bảng: student_management_app_schedule
DROP TABLE IF EXISTS `student_management_app_schedule`;
CREATE TABLE `student_management_app_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weekday` int(11) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `room` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `session_year_id_id` int(11) NOT NULL,
  `subject_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_session_year_id_id_64f0dfd7_fk_student_m` (`session_year_id_id`),
  KEY `student_management_a_subject_id_id_2aa02d4c_fk_student_m` (`subject_id_id`),
  CONSTRAINT `student_management_a_session_year_id_id_64f0dfd7_fk_student_m` FOREIGN KEY (`session_year_id_id`) REFERENCES `student_management_app_sessionyearmodel` (`id`),
  CONSTRAINT `student_management_a_subject_id_id_2aa02d4c_fk_student_m` FOREIGN KEY (`subject_id_id`) REFERENCES `student_management_app_subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dữ liệu cho bảng `student_management_app_schedule`
LOCK TABLES `student_management_app_schedule` WRITE;
INSERT INTO `student_management_app_schedule` (`id`, `weekday`, `start_time`, `end_time`, `room`, `created_at`, `updated_at`, `session_year_id_id`, `subject_id_id`) VALUES
(144, 2, '13:00:00', '16:50:00', 'B207', '2025-10-20 10:58:23.643225', '2025-10-20 10:58:23.643240', 1, 15),
(145, 5, '8:00:00', '11:50:00', 'A109', '2025-10-20 10:58:23.696302', '2025-10-20 10:58:23.696318', 1, 17),
(146, 1, '15:00:00', '17:50:00', 'B204', '2025-10-20 10:58:23.736343', '2025-10-20 10:58:23.736357', 1, 1),
(147, 0, '9:00:00', '11:50:00', 'A102', '2025-10-20 10:58:23.785999', '2025-10-20 10:58:23.786012', 1, 2),
(148, 1, '8:00:00', '10:50:00', 'A110', '2025-10-20 10:58:23.799638', '2025-10-20 10:58:23.799652', 1, 3),
(149, 3, '15:00:00', '17:50:00', 'A106', '2025-10-20 10:58:23.846876', '2025-10-20 10:58:23.846891', 1, 4),
(150, 0, '14:00:00', '16:50:00', 'A102', '2025-10-20 10:58:23.913761', '2025-10-20 10:58:23.913775', 1, 5),
(151, 5, '17:00:00', '19:50:00', 'B214', '2025-10-20 10:58:24.017691', '2025-10-20 10:58:24.017704', 1, 6),
(152, 2, '7:00:00', '9:50:00', 'B210', '2025-10-20 10:58:24.097243', '2025-10-20 10:58:24.097257', 1, 7),
(153, 3, '9:00:00', '11:50:00', 'B204', '2025-10-20 10:58:24.143804', '2025-10-20 10:58:24.143819', 1, 8),
(154, 5, '13:00:00', '15:50:00', 'C307', '2025-10-20 10:58:24.183996', '2025-10-20 10:58:24.184009', 1, 9),
(155, 4, '14:00:00', '16:50:00', 'A101', '2025-10-20 10:58:24.238656', '2025-10-20 10:58:24.238670', 1, 10),
(156, 4, '9:00:00', '11:50:00', 'A111', '2025-10-20 10:58:24.261901', '2025-10-20 10:58:24.261914', 1, 11),
(157, 1, '9:00:00', '11:50:00', 'B213', '2025-10-20 10:58:24.403606', '2025-10-20 10:58:24.403619', 1, 12),
(158, 5, '13:00:00', '15:50:00', 'A109', '2025-10-20 10:58:24.443907', '2025-10-20 10:58:24.443923', 1, 13),
(159, 0, '13:00:00', '15:50:00', 'A112', '2025-10-20 10:58:24.552478', '2025-10-20 10:58:24.552492', 1, 14),
(160, 3, '17:00:00', '19:50:00', 'C302', '2025-10-20 10:58:24.594239', '2025-10-20 10:58:24.594254', 1, 16),
(161, 2, '17:00:00', '19:50:00', 'B205', '2025-10-20 10:58:24.816481', '2025-10-20 10:58:24.816494', 1, 18),
(162, 0, '17:00:00', '19:50:00', 'B212', '2025-10-20 10:58:25.040031', '2025-10-20 10:58:25.040044', 1, 19);
UNLOCK TABLES;


-- Bảng: student_management_app_sessionyearmodel
DROP TABLE IF EXISTS `student_management_app_sessionyearmodel`;
CREATE TABLE `student_management_app_sessionyearmodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_start_year` date NOT NULL,
  `session_end_year` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_sessionyearmodel`
LOCK TABLES `student_management_app_sessionyearmodel` WRITE;
INSERT INTO `student_management_app_sessionyearmodel` (`id`, `session_start_year`, `session_end_year`) VALUES
(1, '2020-01-01', '2023-01-01'),
(2, '2020-01-01', '2022-01-01'),
(3, '2024-01-01', '2024-12-31');
UNLOCK TABLES;


-- Bảng: student_management_app_staffs
DROP TABLE IF EXISTS `student_management_app_staffs`;
CREATE TABLE `student_management_app_staffs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `fcm_token` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_id` (`admin_id`),
  CONSTRAINT `student_management_a_admin_id_5bfdd57d_fk_student_m` FOREIGN KEY (`admin_id`) REFERENCES `student_management_app_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_staffs`
LOCK TABLES `student_management_app_staffs` WRITE;
INSERT INTO `student_management_app_staffs` (`id`, `address`, `created_at`, `updated_at`, `admin_id`, `fcm_token`) VALUES
(1, 'Staff One Address 1', '2020-04-12 08:38:05.762808', '2020-04-12 08:38:05.762808', 2, ''),
(2, 'Staff Two Address', '2020-04-12 08:38:30.048488', '2020-04-12 08:38:30.049488', 3, ''),
(3, 'Staff Three Address', '2020-04-12 08:38:51.316112', '2020-04-12 08:38:51.316112', 4, ''),
(4, 'Staff Four Address', '2020-04-12 08:39:17.451888', '2020-04-12 08:39:17.451888', 5, ''),
(5, 'Test Address', '2025-10-20 09:22:59.012272', '2025-10-20 09:22:59.012286', 17, '');
UNLOCK TABLES;


-- Bảng: student_management_app_studentenrollment
DROP TABLE IF EXISTS `student_management_app_studentenrollment`;
CREATE TABLE `student_management_app_studentenrollment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enrollment_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `session_year_id_id` int(11) NOT NULL,
  `student_id_id` int(11) NOT NULL,
  `subject_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_management_app_s_student_id_id_subject_id_bf3d8d9f_uniq` (`student_id_id`,`subject_id_id`,`session_year_id_id`),
  KEY `student_management_a_session_year_id_id_cbddb80b_fk_student_m` (`session_year_id_id`),
  KEY `student_management_a_subject_id_id_f8c3ec2a_fk_student_m` (`subject_id_id`),
  CONSTRAINT `student_management_a_session_year_id_id_cbddb80b_fk_student_m` FOREIGN KEY (`session_year_id_id`) REFERENCES `student_management_app_sessionyearmodel` (`id`),
  CONSTRAINT `student_management_a_student_id_id_2f60e405_fk_student_m` FOREIGN KEY (`student_id_id`) REFERENCES `student_management_app_students` (`id`),
  CONSTRAINT `student_management_a_subject_id_id_f8c3ec2a_fk_student_m` FOREIGN KEY (`subject_id_id`) REFERENCES `student_management_app_subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1702 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dữ liệu cho bảng `student_management_app_studentenrollment`
LOCK TABLES `student_management_app_studentenrollment` WRITE;
INSERT INTO `student_management_app_studentenrollment` (`id`, `enrollment_date`, `is_active`, `created_at`, `updated_at`, `session_year_id_id`, `student_id_id`, `subject_id_id`) VALUES
(1531, '2025-10-20 10:58:23.262207', 1, '2025-10-20 10:58:23.262240', '2025-10-20 10:58:23.262250', 1, 2, 5),
(1532, '2025-10-20 10:58:23.264092', 1, '2025-10-20 10:58:23.264115', '2025-10-20 10:58:23.264123', 1, 2, 9),
(1533, '2025-10-20 10:58:23.266027', 1, '2025-10-20 10:58:23.266056', '2025-10-20 10:58:23.266065', 1, 2, 6),
(1534, '2025-10-20 10:58:23.267904', 1, '2025-10-20 10:58:23.267923', '2025-10-20 10:58:23.267929', 1, 2, 12),
(1535, '2025-10-20 10:58:23.269660', 1, '2025-10-20 10:58:23.269680', '2025-10-20 10:58:23.269686', 1, 2, 7),
(1536, '2025-10-20 10:58:23.272651', 1, '2025-10-20 10:58:23.272670', '2025-10-20 10:58:23.272676', 1, 3, 18),
(1537, '2025-10-20 10:58:23.274569', 1, '2025-10-20 10:58:23.274591', '2025-10-20 10:58:23.274597', 1, 3, 19),
(1538, '2025-10-20 10:58:23.276449', 1, '2025-10-20 10:58:23.276479', '2025-10-20 10:58:23.276486', 1, 3, 4),
(1539, '2025-10-20 10:58:23.278239', 1, '2025-10-20 10:58:23.278258', '2025-10-20 10:58:23.278264', 1, 3, 15),
(1540, '2025-10-20 10:58:23.279915', 1, '2025-10-20 10:58:23.279930', '2025-10-20 10:58:23.279936', 1, 3, 1),
(1541, '2025-10-20 10:58:23.281667', 1, '2025-10-20 10:58:23.281688', '2025-10-20 10:58:23.281694', 1, 3, 12),
(1542, '2025-10-20 10:58:23.283636', 1, '2025-10-20 10:58:23.283659', '2025-10-20 10:58:23.283665', 1, 3, 6),
(1543, '2025-10-20 10:58:23.286709', 1, '2025-10-20 10:58:23.286732', '2025-10-20 10:58:23.286739', 1, 4, 19),
(1544, '2025-10-20 10:58:23.288482', 1, '2025-10-20 10:58:23.288499', '2025-10-20 10:58:23.288504', 1, 4, 14),
(1545, '2025-10-20 10:58:23.290243', 1, '2025-10-20 10:58:23.290265', '2025-10-20 10:58:23.290275', 1, 4, 12),
(1546, '2025-10-20 10:58:23.291961', 1, '2025-10-20 10:58:23.291980', '2025-10-20 10:58:23.291986', 1, 4, 7),
(1547, '2025-10-20 10:58:23.294027', 1, '2025-10-20 10:58:23.294045', '2025-10-20 10:58:23.294051', 1, 4, 4),
(1548, '2025-10-20 10:58:23.296524', 1, '2025-10-20 10:58:23.296547', '2025-10-20 10:58:23.296552', 1, 4, 1),
(1549, '2025-10-20 10:58:23.298916', 1, '2025-10-20 10:58:23.298939', '2025-10-20 10:58:23.298945', 1, 4, 9),
(1550, '2025-10-20 10:58:23.302005', 1, '2025-10-20 10:58:23.302025', '2025-10-20 10:58:23.302031', 1, 5, 7),
(1551, '2025-10-20 10:58:23.304531', 1, '2025-10-20 10:58:23.304552', '2025-10-20 10:58:23.304558', 1, 5, 18),
(1552, '2025-10-20 10:58:23.306317', 1, '2025-10-20 10:58:23.306336', '2025-10-20 10:58:23.306342', 1, 5, 12),
(1553, '2025-10-20 10:58:23.308222', 1, '2025-10-20 10:58:23.308243', '2025-10-20 10:58:23.308250', 1, 5, 17),
(1554, '2025-10-20 10:58:23.309977', 1, '2025-10-20 10:58:23.309996', '2025-10-20 10:58:23.310002', 1, 5, 8),
(1555, '2025-10-20 10:58:23.311702', 1, '2025-10-20 10:58:23.311729', '2025-10-20 10:58:23.311739', 1, 5, 15),
(1556, '2025-10-20 10:58:23.313639', 1, '2025-10-20 10:58:23.313661', '2025-10-20 10:58:23.313667', 1, 5, 6),
(1557, '2025-10-20 10:58:23.316479', 1, '2025-10-20 10:58:23.316499', '2025-10-20 10:58:23.316507', 1, 6, 17),
(1558, '2025-10-20 10:58:23.318132', 1, '2025-10-20 10:58:23.318148', '2025-10-20 10:58:23.318155', 1, 6, 8),
(1559, '2025-10-20 10:58:23.319803', 1, '2025-10-20 10:58:23.319821', '2025-10-20 10:58:23.319827', 1, 6, 18),
(1560, '2025-10-20 10:58:23.321463', 1, '2025-10-20 10:58:23.321478', '2025-10-20 10:58:23.321484', 1, 6, 1),
(1561, '2025-10-20 10:58:23.323155', 1, '2025-10-20 10:58:23.323169', '2025-10-20 10:58:23.323176', 1, 6, 13),
(1562, '2025-10-20 10:58:23.325603', 1, '2025-10-20 10:58:23.325622', '2025-10-20 10:58:23.325629', 1, 7, 18),
(1563, '2025-10-20 10:58:23.327362', 1, '2025-10-20 10:58:23.327379', '2025-10-20 10:58:23.327385', 1, 7, 15),
(1564, '2025-10-20 10:58:23.328864', 1, '2025-10-20 10:58:23.328877', '2025-10-20 10:58:23.328882', 1, 7, 1),
(1565, '2025-10-20 10:58:23.330410', 1, '2025-10-20 10:58:23.330423', '2025-10-20 10:58:23.330428', 1, 7, 14),
(1566, '2025-10-20 10:58:23.331965', 1, '2025-10-20 10:58:23.331982', '2025-10-20 10:58:23.331989', 1, 7, 7),
(1567, '2025-10-20 10:58:23.334564', 1, '2025-10-20 10:58:23.334586', '2025-10-20 10:58:23.334594', 1, 8, 1),
(1568, '2025-10-20 10:58:23.336722', 1, '2025-10-20 10:58:23.336743', '2025-10-20 10:58:23.336749', 1, 8, 18),
(1569, '2025-10-20 10:58:23.338504', 1, '2025-10-20 10:58:23.338519', '2025-10-20 10:58:23.338525', 1, 8, 5),
(1570, '2025-10-20 10:58:23.340325', 1, '2025-10-20 10:58:23.340344', '2025-10-20 10:58:23.340350', 1, 8, 13),
(1571, '2025-10-20 10:58:23.341986', 1, '2025-10-20 10:58:23.342002', '2025-10-20 10:58:23.342008', 1, 8, 10),
(1572, '2025-10-20 10:58:23.344861', 1, '2025-10-20 10:58:23.344880', '2025-10-20 10:58:23.344886', 1, 9, 10),
(1573, '2025-10-20 10:58:23.346654', 1, '2025-10-20 10:58:23.346675', '2025-10-20 10:58:23.346680', 1, 9, 12),
(1574, '2025-10-20 10:58:23.348448', 1, '2025-10-20 10:58:23.348467', '2025-10-20 10:58:23.348472', 1, 9, 7),
(1575, '2025-10-20 10:58:23.350076', 1, '2025-10-20 10:58:23.350092', '2025-10-20 10:58:23.350099', 1, 9, 5),
(1576, '2025-10-20 10:58:23.351629', 1, '2025-10-20 10:58:23.351641', '2025-10-20 10:58:23.351646', 1, 9, 18),
(1577, '2025-10-20 10:58:23.353216', 1, '2025-10-20 10:58:23.353233', '2025-10-20 10:58:23.353240', 1, 9, 6),
(1578, '2025-10-20 10:58:23.354927', 1, '2025-10-20 10:58:23.354943', '2025-10-20 10:58:23.354949', 1, 9, 9),
(1579, '2025-10-20 10:58:23.357271', 1, '2025-10-20 10:58:23.357286', '2025-10-20 10:58:23.357292', 1, 10, 16),
(1580, '2025-10-20 10:58:23.358854', 1, '2025-10-20 10:58:23.358867', '2025-10-20 10:58:23.358873', 1, 10, 7),
(1581, '2025-10-20 10:58:23.360433', 1, '2025-10-20 10:58:23.360449', '2025-10-20 10:58:23.360455', 1, 10, 5),
(1582, '2025-10-20 10:58:23.362174', 1, '2025-10-20 10:58:23.362191', '2025-10-20 10:58:23.362197', 1, 10, 10),
(1583, '2025-10-20 10:58:23.363748', 1, '2025-10-20 10:58:23.363764', '2025-10-20 10:58:23.363770', 1, 10, 8),
(1584, '2025-10-20 10:58:23.365409', 1, '2025-10-20 10:58:23.365425', '2025-10-20 10:58:23.365431', 1, 10, 15),
(1585, '2025-10-20 10:58:23.366979', 1, '2025-10-20 10:58:23.366994', '2025-10-20 10:58:23.367000', 1, 10, 17),
(1586, '2025-10-20 10:58:23.369649', 1, '2025-10-20 10:58:23.369668', '2025-10-20 10:58:23.369674', 1, 11, 8),
(1587, '2025-10-20 10:58:23.371347', 1, '2025-10-20 10:58:23.371362', '2025-10-20 10:58:23.371368', 1, 11, 3),
(1588, '2025-10-20 10:58:23.372915', 1, '2025-10-20 10:58:23.372928', '2025-10-20 10:58:23.372933', 1, 11, 19),
(1589, '2025-10-20 10:58:23.374497', 1, '2025-10-20 10:58:23.374513', '2025-10-20 10:58:23.374519', 1, 11, 4),
(1590, '2025-10-20 10:58:23.376514', 1, '2025-10-20 10:58:23.376536', '2025-10-20 10:58:23.376541', 1, 11, 17),
(1591, '2025-10-20 10:58:23.378159', 1, '2025-10-20 10:58:23.378172', '2025-10-20 10:58:23.378177', 1, 11, 13),
(1592, '2025-10-20 10:58:23.380611', 1, '2025-10-20 10:58:23.380627', '2025-10-20 10:58:23.380634', 1, 12, 10),
(1593, '2025-10-20 10:58:23.382462', 1, '2025-10-20 10:58:23.382483', '2025-10-20 10:58:23.382489', 1, 12, 2),
(1594, '2025-10-20 10:58:23.384173', 1, '2025-10-20 10:58:23.384188', '2025-10-20 10:58:23.384193', 1, 12, 6),
(1595, '2025-10-20 10:58:23.385703', 1, '2025-10-20 10:58:23.385714', '2025-10-20 10:58:23.385719', 1, 12, 18),
(1596, '2025-10-20 10:58:23.387212', 1, '2025-10-20 10:58:23.387227', '2025-10-20 10:58:23.387233', 1, 12, 7),
(1597, '2025-10-20 10:58:23.388911', 1, '2025-10-20 10:58:23.388931', '2025-10-20 10:58:23.388937', 1, 12, 12),
(1598, '2025-10-20 10:58:23.390707', 1, '2025-10-20 10:58:23.390725', '2025-10-20 10:58:23.390731', 1, 12, 5),
(1599, '2025-10-20 10:58:23.393124', 1, '2025-10-20 10:58:23.393142', '2025-10-20 10:58:23.393150', 1, 13, 4),
(1600, '2025-10-20 10:58:23.395034', 1, '2025-10-20 10:58:23.395052', '2025-10-20 10:58:23.395057', 1, 13, 2),
(1601, '2025-10-20 10:58:23.396811', 1, '2025-10-20 10:58:23.396830', '2025-10-20 10:58:23.396836', 1, 13, 5),
(1602, '2025-10-20 10:58:23.398698', 1, '2025-10-20 10:58:23.398714', '2025-10-20 10:58:23.398721', 1, 13, 7),
(1603, '2025-10-20 10:58:23.400501', 1, '2025-10-20 10:58:23.400513', '2025-10-20 10:58:23.400518', 1, 13, 17),
(1604, '2025-10-20 10:58:23.402151', 1, '2025-10-20 10:58:23.402175', '2025-10-20 10:58:23.402185', 1, 13, 1),
(1605, '2025-10-20 10:58:23.404737', 1, '2025-10-20 10:58:23.404756', '2025-10-20 10:58:23.404763', 1, 14, 13),
(1606, '2025-10-20 10:58:23.406274', 1, '2025-10-20 10:58:23.406288', '2025-10-20 10:58:23.406294', 1, 14, 19),
(1607, '2025-10-20 10:58:23.407805', 1, '2025-10-20 10:58:23.407817', '2025-10-20 10:58:23.407822', 1, 14, 8),
(1608, '2025-10-20 10:58:23.409455', 1, '2025-10-20 10:58:23.409479', '2025-10-20 10:58:23.409488', 1, 14, 7),
(1609, '2025-10-20 10:58:23.411243', 1, '2025-10-20 10:58:23.411260', '2025-10-20 10:58:23.411266', 1, 14, 18),
(1610, '2025-10-20 10:58:23.412826', 1, '2025-10-20 10:58:23.412839', '2025-10-20 10:58:23.412845', 1, 14, 4),
(1611, '2025-10-20 10:58:23.415132', 1, '2025-10-20 10:58:23.415148', '2025-10-20 10:58:23.415155', 1, 15, 5),
(1612, '2025-10-20 10:58:23.416969', 1, '2025-10-20 10:58:23.416991', '2025-10-20 10:58:23.416997', 1, 15, 9),
(1613, '2025-10-20 10:58:23.418782', 1, '2025-10-20 10:58:23.418799', '2025-10-20 10:58:23.418805', 1, 15, 6),
(1614, '2025-10-20 10:58:23.420382', 1, '2025-10-20 10:58:23.420396', '2025-10-20 10:58:23.420402', 1, 15, 7),
(1615, '2025-10-20 10:58:23.421975', 1, '2025-10-20 10:58:23.421991', '2025-10-20 10:58:23.421998', 1, 15, 2),
(1616, '2025-10-20 10:58:23.423827', 1, '2025-10-20 10:58:23.423853', '2025-10-20 10:58:23.423859', 1, 15, 8),
(1617, '2025-10-20 10:58:23.426449', 1, '2025-10-20 10:58:23.426470', '2025-10-20 10:58:23.426477', 1, 16, 12),
(1618, '2025-10-20 10:58:23.428069', 1, '2025-10-20 10:58:23.428082', '2025-10-20 10:58:23.428087', 1, 16, 18),
(1619, '2025-10-20 10:58:23.429701', 1, '2025-10-20 10:58:23.429718', '2025-10-20 10:58:23.429729', 1, 16, 10),
(1620, '2025-10-20 10:58:23.431422', 1, '2025-10-20 10:58:23.431437', '2025-10-20 10:58:23.431442', 1, 16, 7),
(1621, '2025-10-20 10:58:23.433039', 1, '2025-10-20 10:58:23.433051', '2025-10-20 10:58:23.433056', 1, 16, 17),
(1622, '2025-10-20 10:58:23.434887', 1, '2025-10-20 10:58:23.434901', '2025-10-20 10:58:23.434907', 1, 16, 19),
(1623, '2025-10-20 10:58:23.436762', 1, '2025-10-20 10:58:23.436782', '2025-10-20 10:58:23.436789', 1, 16, 16),
(1624, '2025-10-20 10:58:23.439488', 1, '2025-10-20 10:58:23.439506', '2025-10-20 10:58:23.439512', 1, 17, 2),
(1625, '2025-10-20 10:58:23.441384', 1, '2025-10-20 10:58:23.441401', '2025-10-20 10:58:23.441408', 1, 17, 19),
(1626, '2025-10-20 10:58:23.443328', 1, '2025-10-20 10:58:23.443345', '2025-10-20 10:58:23.443350', 1, 17, 13),
(1627, '2025-10-20 10:58:23.445523', 1, '2025-10-20 10:58:23.445544', '2025-10-20 10:58:23.445550', 1, 17, 7),
(1628, '2025-10-20 10:58:23.447491', 1, '2025-10-20 10:58:23.447505', '2025-10-20 10:58:23.447510', 1, 17, 5),
(1629, '2025-10-20 10:58:23.449261', 1, '2025-10-20 10:58:23.449275', '2025-10-20 10:58:23.449282', 1, 17, 15),
(1630, '2025-10-20 10:58:23.452203', 1, '2025-10-20 10:58:23.452222', '2025-10-20 10:58:23.452228', 1, 18, 19);
INSERT INTO `student_management_app_studentenrollment` (`id`, `enrollment_date`, `is_active`, `created_at`, `updated_at`, `session_year_id_id`, `student_id_id`, `subject_id_id`) VALUES
(1631, '2025-10-20 10:58:23.454243', 1, '2025-10-20 10:58:23.454263', '2025-10-20 10:58:23.454270', 1, 18, 6),
(1632, '2025-10-20 10:58:23.456138', 1, '2025-10-20 10:58:23.456151', '2025-10-20 10:58:23.456157', 1, 18, 16),
(1633, '2025-10-20 10:58:23.458184', 1, '2025-10-20 10:58:23.458209', '2025-10-20 10:58:23.458219', 1, 18, 2),
(1634, '2025-10-20 10:58:23.460368', 1, '2025-10-20 10:58:23.460388', '2025-10-20 10:58:23.460393', 1, 18, 5),
(1635, '2025-10-20 10:58:23.463111', 1, '2025-10-20 10:58:23.463130', '2025-10-20 10:58:23.463137', 1, 19, 17),
(1636, '2025-10-20 10:58:23.465137', 1, '2025-10-20 10:58:23.465158', '2025-10-20 10:58:23.465164', 1, 19, 2),
(1637, '2025-10-20 10:58:23.467187', 1, '2025-10-20 10:58:23.467207', '2025-10-20 10:58:23.467213', 1, 19, 4),
(1638, '2025-10-20 10:58:23.468842', 1, '2025-10-20 10:58:23.468857', '2025-10-20 10:58:23.468863', 1, 19, 15),
(1639, '2025-10-20 10:58:23.470659', 1, '2025-10-20 10:58:23.470672', '2025-10-20 10:58:23.470678', 1, 19, 6),
(1640, '2025-10-20 10:58:23.473563', 1, '2025-10-20 10:58:23.473583', '2025-10-20 10:58:23.473589', 1, 20, 18),
(1641, '2025-10-20 10:58:23.475532', 1, '2025-10-20 10:58:23.475548', '2025-10-20 10:58:23.475555', 1, 20, 10),
(1642, '2025-10-20 10:58:23.477341', 1, '2025-10-20 10:58:23.477356', '2025-10-20 10:58:23.477362', 1, 20, 16),
(1643, '2025-10-20 10:58:23.479348', 1, '2025-10-20 10:58:23.479366', '2025-10-20 10:58:23.479372', 1, 20, 5),
(1644, '2025-10-20 10:58:23.481037', 1, '2025-10-20 10:58:23.481052', '2025-10-20 10:58:23.481057', 1, 20, 8),
(1645, '2025-10-20 10:58:23.483655', 1, '2025-10-20 10:58:23.483672', '2025-10-20 10:58:23.483679', 1, 21, 11),
(1646, '2025-10-20 10:58:23.485711', 1, '2025-10-20 10:58:23.485731', '2025-10-20 10:58:23.485737', 1, 21, 6),
(1647, '2025-10-20 10:58:23.487686', 1, '2025-10-20 10:58:23.487706', '2025-10-20 10:58:23.487712', 1, 21, 5),
(1648, '2025-10-20 10:58:23.489605', 1, '2025-10-20 10:58:23.489620', '2025-10-20 10:58:23.489628', 1, 21, 15),
(1649, '2025-10-20 10:58:23.491459', 1, '2025-10-20 10:58:23.491474', '2025-10-20 10:58:23.491481', 1, 21, 12),
(1650, '2025-10-20 10:58:23.493528', 1, '2025-10-20 10:58:23.493549', '2025-10-20 10:58:23.493555', 1, 21, 16),
(1651, '2025-10-20 10:58:23.496148', 1, '2025-10-20 10:58:23.496168', '2025-10-20 10:58:23.496175', 1, 22, 14),
(1652, '2025-10-20 10:58:23.497813', 1, '2025-10-20 10:58:23.497827', '2025-10-20 10:58:23.497833', 1, 22, 19),
(1653, '2025-10-20 10:58:23.499479', 1, '2025-10-20 10:58:23.499500', '2025-10-20 10:58:23.499508', 1, 22, 1),
(1654, '2025-10-20 10:58:23.501270', 1, '2025-10-20 10:58:23.501289', '2025-10-20 10:58:23.501295', 1, 22, 11),
(1655, '2025-10-20 10:58:23.502942', 1, '2025-10-20 10:58:23.502955', '2025-10-20 10:58:23.502961', 1, 22, 6),
(1656, '2025-10-20 10:58:23.504499', 1, '2025-10-20 10:58:23.504510', '2025-10-20 10:58:23.504515', 1, 22, 15),
(1657, '2025-10-20 10:58:23.506072', 1, '2025-10-20 10:58:23.506085', '2025-10-20 10:58:23.506090', 1, 22, 3),
(1658, '2025-10-20 10:58:23.508855', 1, '2025-10-20 10:58:23.508877', '2025-10-20 10:58:23.508884', 1, 23, 18),
(1659, '2025-10-20 10:58:23.510600', 1, '2025-10-20 10:58:23.510615', '2025-10-20 10:58:23.510621', 1, 23, 4),
(1660, '2025-10-20 10:58:23.512193', 1, '2025-10-20 10:58:23.512204', '2025-10-20 10:58:23.512210', 1, 23, 2),
(1661, '2025-10-20 10:58:23.513882', 1, '2025-10-20 10:58:23.513903', '2025-10-20 10:58:23.513908', 1, 23, 6),
(1662, '2025-10-20 10:58:23.515654', 1, '2025-10-20 10:58:23.515673', '2025-10-20 10:58:23.515678', 1, 23, 5),
(1663, '2025-10-20 10:58:23.517330', 1, '2025-10-20 10:58:23.517346', '2025-10-20 10:58:23.517352', 1, 23, 15),
(1664, '2025-10-20 10:58:23.520048', 1, '2025-10-20 10:58:23.520072', '2025-10-20 10:58:23.520082', 1, 24, 6),
(1665, '2025-10-20 10:58:23.522021', 1, '2025-10-20 10:58:23.522044', '2025-10-20 10:58:23.522050', 1, 24, 8),
(1666, '2025-10-20 10:58:23.523747', 1, '2025-10-20 10:58:23.523760', '2025-10-20 10:58:23.523766', 1, 24, 18),
(1667, '2025-10-20 10:58:23.525304', 1, '2025-10-20 10:58:23.525317', '2025-10-20 10:58:23.525324', 1, 24, 13),
(1668, '2025-10-20 10:58:23.526945', 1, '2025-10-20 10:58:23.526961', '2025-10-20 10:58:23.526968', 1, 24, 12),
(1669, '2025-10-20 10:58:23.528629', 1, '2025-10-20 10:58:23.528644', '2025-10-20 10:58:23.528650', 1, 24, 4),
(1670, '2025-10-20 10:58:23.531091', 1, '2025-10-20 10:58:23.531109', '2025-10-20 10:58:23.531116', 1, 25, 15),
(1671, '2025-10-20 10:58:23.532773', 1, '2025-10-20 10:58:23.532787', '2025-10-20 10:58:23.532792', 1, 25, 10),
(1672, '2025-10-20 10:58:23.534404', 1, '2025-10-20 10:58:23.534421', '2025-10-20 10:58:23.534426', 1, 25, 7),
(1673, '2025-10-20 10:58:23.536135', 1, '2025-10-20 10:58:23.536152', '2025-10-20 10:58:23.536158', 1, 25, 13),
(1674, '2025-10-20 10:58:23.537798', 1, '2025-10-20 10:58:23.537816', '2025-10-20 10:58:23.537823', 1, 25, 17),
(1675, '2025-10-20 10:58:23.539428', 1, '2025-10-20 10:58:23.539442', '2025-10-20 10:58:23.539449', 1, 25, 16),
(1676, '2025-10-20 10:58:23.541145', 1, '2025-10-20 10:58:23.541169', '2025-10-20 10:58:23.541175', 1, 25, 6),
(1677, '2025-10-20 10:58:23.543980', 1, '2025-10-20 10:58:23.544000', '2025-10-20 10:58:23.544007', 1, 26, 6),
(1678, '2025-10-20 10:58:23.545697', 1, '2025-10-20 10:58:23.545713', '2025-10-20 10:58:23.545720', 1, 26, 19),
(1679, '2025-10-20 10:58:23.547328', 1, '2025-10-20 10:58:23.547344', '2025-10-20 10:58:23.547351', 1, 26, 17),
(1680, '2025-10-20 10:58:23.549033', 1, '2025-10-20 10:58:23.549051', '2025-10-20 10:58:23.549057', 1, 26, 2),
(1681, '2025-10-20 10:58:23.550971', 1, '2025-10-20 10:58:23.550987', '2025-10-20 10:58:23.550992', 1, 26, 4),
(1682, '2025-10-20 10:58:23.552563', 1, '2025-10-20 10:58:23.552576', '2025-10-20 10:58:23.552581', 1, 26, 5),
(1683, '2025-10-20 10:58:23.554161', 1, '2025-10-20 10:58:23.554177', '2025-10-20 10:58:23.554185', 1, 26, 7),
(1684, '2025-10-20 10:58:23.556811', 1, '2025-10-20 10:58:23.556831', '2025-10-20 10:58:23.556837', 1, 27, 18),
(1685, '2025-10-20 10:58:23.558545', 1, '2025-10-20 10:58:23.558561', '2025-10-20 10:58:23.558567', 1, 27, 2),
(1686, '2025-10-20 10:58:23.560108', 1, '2025-10-20 10:58:23.560120', '2025-10-20 10:58:23.560125', 1, 27, 7),
(1687, '2025-10-20 10:58:23.561620', 1, '2025-10-20 10:58:23.561637', '2025-10-20 10:58:23.561644', 1, 27, 11),
(1688, '2025-10-20 10:58:23.563534', 1, '2025-10-20 10:58:23.563568', '2025-10-20 10:58:23.563578', 1, 27, 1),
(1689, '2025-10-20 10:58:23.565389', 1, '2025-10-20 10:58:23.565407', '2025-10-20 10:58:23.565414', 1, 27, 8),
(1690, '2025-10-20 10:58:23.567064', 1, '2025-10-20 10:58:23.567078', '2025-10-20 10:58:23.567083', 1, 27, 14),
(1691, '2025-10-20 10:58:23.569826', 1, '2025-10-20 10:58:23.569845', '2025-10-20 10:58:23.569851', 1, 28, 2),
(1692, '2025-10-20 10:58:23.571686', 1, '2025-10-20 10:58:23.571706', '2025-10-20 10:58:23.571713', 1, 28, 13),
(1693, '2025-10-20 10:58:23.573331', 1, '2025-10-20 10:58:23.573343', '2025-10-20 10:58:23.573349', 1, 28, 12),
(1694, '2025-10-20 10:58:23.574899', 1, '2025-10-20 10:58:23.574913', '2025-10-20 10:58:23.574922', 1, 28, 5),
(1695, '2025-10-20 10:58:23.576655', 1, '2025-10-20 10:58:23.576680', '2025-10-20 10:58:23.576690', 1, 28, 11),
(1696, '2025-10-20 10:58:23.578520', 1, '2025-10-20 10:58:23.578542', '2025-10-20 10:58:23.578549', 1, 28, 16),
(1697, '2025-10-20 10:58:23.581021', 1, '2025-10-20 10:58:23.581038', '2025-10-20 10:58:23.581046', 1, 29, 10),
(1698, '2025-10-20 10:58:23.582774', 1, '2025-10-20 10:58:23.582792', '2025-10-20 10:58:23.582799', 1, 29, 19),
(1699, '2025-10-20 10:58:23.584540', 1, '2025-10-20 10:58:23.584558', '2025-10-20 10:58:23.584563', 1, 29, 16),
(1700, '2025-10-20 10:58:23.586181', 1, '2025-10-20 10:58:23.586193', '2025-10-20 10:58:23.586199', 1, 29, 9),
(1701, '2025-10-20 10:58:23.587744', 1, '2025-10-20 10:58:23.587757', '2025-10-20 10:58:23.587764', 1, 29, 6);
UNLOCK TABLES;


-- Bảng: student_management_app_studentresult
DROP TABLE IF EXISTS `student_management_app_studentresult`;
CREATE TABLE `student_management_app_studentresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id_id` int(11) NOT NULL,
  `subject_id_id` int(11) NOT NULL,
  `subject_exam_marks` float DEFAULT 0,
  `subject_assignment_marks` float DEFAULT 0,
  `created_at` date NOT NULL,
  `updated_at` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id_id` (`student_id_id`),
  KEY `subject_id_id` (`subject_id_id`),
  CONSTRAINT `student_management_app_studentresult_ibfk_1` FOREIGN KEY (`student_id_id`) REFERENCES `student_management_app_students` (`id`) ON DELETE CASCADE,
  CONSTRAINT `student_management_app_studentresult_ibfk_2` FOREIGN KEY (`subject_id_id`) REFERENCES `student_management_app_subjects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_studentresult`
LOCK TABLES `student_management_app_studentresult` WRITE;
INSERT INTO `student_management_app_studentresult` (`id`, `student_id_id`, `subject_id_id`, `subject_exam_marks`, `subject_assignment_marks`, `created_at`, `updated_at`) VALUES
(1, 2, 5, 57.3, 30.3, '2025-10-20', '2025-10-20'),
(2, 2, 6, 41.5, 27.2, '2025-10-20', '2025-10-20'),
(3, 2, 7, 45.2, 28.9, '2025-10-20', '2025-10-20'),
(4, 2, 9, 51.0, 27.1, '2025-10-20', '2025-10-20'),
(5, 2, 12, 27.0, 34.7, '2025-10-20', '2025-10-20'),
(6, 3, 1, 45.1, 32.2, '2025-10-20', '2025-10-20'),
(7, 3, 4, 47.5, 31.9, '2025-10-20', '2025-10-20'),
(8, 3, 6, 49.0, 30.9, '2025-10-20', '2025-10-20'),
(9, 3, 12, 49.1, 33.3, '2025-10-20', '2025-10-20'),
(10, 3, 15, 36.4, 31.0, '2025-10-20', '2025-10-20'),
(11, 3, 18, 44.2, 40.0, '2025-10-20', '2025-10-20'),
(12, 3, 19, 42.8, 32.1, '2025-10-20', '2025-10-20'),
(13, 4, 1, 39.2, 28.6, '2025-10-20', '2025-10-20'),
(14, 4, 4, 45.7, 25.0, '2025-10-20', '2025-10-20'),
(15, 4, 7, 41.9, 26.0, '2025-10-20', '2025-10-20'),
(16, 4, 9, 53.7, 30.9, '2025-10-20', '2025-10-20'),
(17, 4, 12, 26.8, 23.2, '2025-10-20', '2025-10-20'),
(18, 4, 14, 53.1, 26.0, '2025-10-20', '2025-10-20'),
(19, 4, 19, 53.7, 27.6, '2025-10-20', '2025-10-20'),
(20, 5, 6, 35.4, 32.1, '2025-10-20', '2025-10-20'),
(21, 5, 7, 58.0, 34.3, '2025-10-20', '2025-10-20'),
(22, 5, 8, 54.7, 29.7, '2025-10-20', '2025-10-20'),
(23, 5, 12, 41.1, 31.7, '2025-10-20', '2025-10-20'),
(24, 5, 15, 35.3, 26.6, '2025-10-20', '2025-10-20'),
(25, 5, 17, 55.2, 29.6, '2025-10-20', '2025-10-20'),
(26, 5, 18, 38.0, 27.1, '2025-10-20', '2025-10-20'),
(27, 6, 1, 25.4, 28.5, '2025-10-20', '2025-10-20'),
(28, 6, 8, 43.1, 34.7, '2025-10-20', '2025-10-20'),
(29, 6, 13, 55.7, 38.1, '2025-10-20', '2025-10-20'),
(30, 6, 17, 30.4, 21.3, '2025-10-20', '2025-10-20'),
(31, 6, 18, 21.0, 32.4, '2025-10-20', '2025-10-20'),
(32, 7, 1, 48.4, 27.7, '2025-10-20', '2025-10-20'),
(33, 7, 7, 52.3, 37.0, '2025-10-20', '2025-10-20'),
(34, 7, 14, 41.8, 37.3, '2025-10-20', '2025-10-20'),
(35, 7, 15, 59.9, 35.5, '2025-10-20', '2025-10-20'),
(36, 7, 18, 35.5, 36.3, '2025-10-20', '2025-10-20'),
(37, 8, 1, 37.7, 27.2, '2025-10-20', '2025-10-20'),
(38, 8, 5, 45.8, 32.6, '2025-10-20', '2025-10-20'),
(39, 8, 10, 53.2, 38.8, '2025-10-20', '2025-10-20'),
(40, 8, 13, 59.2, 26.1, '2025-10-20', '2025-10-20'),
(41, 8, 18, 54.0, 18.7, '2025-10-20', '2025-10-20'),
(42, 9, 5, 54.6, 29.9, '2025-10-20', '2025-10-20'),
(43, 9, 6, 38.2, 27.6, '2025-10-20', '2025-10-20'),
(44, 9, 7, 36.5, 29.1, '2025-10-20', '2025-10-20'),
(45, 9, 9, 55.6, 32.9, '2025-10-20', '2025-10-20'),
(46, 9, 10, 44.1, 32.0, '2025-10-20', '2025-10-20'),
(47, 9, 12, 53.3, 30.5, '2025-10-20', '2025-10-20'),
(48, 9, 18, 40.5, 35.3, '2025-10-20', '2025-10-20'),
(49, 10, 5, 52.7, 17.9, '2025-10-20', '2025-10-20'),
(50, 10, 7, 43.9, 32.3, '2025-10-20', '2025-10-20'),
(51, 10, 8, 47.9, 33.0, '2025-10-20', '2025-10-20'),
(52, 10, 10, 43.5, 29.7, '2025-10-20', '2025-10-20'),
(53, 10, 15, 37.8, 37.9, '2025-10-20', '2025-10-20'),
(54, 10, 16, 50.7, 24.5, '2025-10-20', '2025-10-20'),
(55, 10, 17, 39.9, 32.7, '2025-10-20', '2025-10-20'),
(56, 11, 3, 21.9, 32.1, '2025-10-20', '2025-10-20'),
(57, 11, 4, 41.9, 38.5, '2025-10-20', '2025-10-20'),
(58, 11, 8, 53.0, 17.5, '2025-10-20', '2025-10-20'),
(59, 11, 13, 46.1, 32.6, '2025-10-20', '2025-10-20'),
(60, 11, 17, 39.4, 33.8, '2025-10-20', '2025-10-20'),
(61, 11, 19, 55.8, 31.4, '2025-10-20', '2025-10-20'),
(62, 12, 2, 44.5, 32.9, '2025-10-20', '2025-10-20'),
(63, 12, 5, 46.6, 28.2, '2025-10-20', '2025-10-20'),
(64, 12, 6, 51.8, 29.5, '2025-10-20', '2025-10-20'),
(65, 12, 7, 37.2, 38.2, '2025-10-20', '2025-10-20'),
(66, 12, 10, 47.6, 39.8, '2025-10-20', '2025-10-20'),
(67, 12, 12, 41.7, 34.3, '2025-10-20', '2025-10-20'),
(68, 12, 18, 59.6, 34.0, '2025-10-20', '2025-10-20'),
(69, 13, 1, 41.3, 28.4, '2025-10-20', '2025-10-20'),
(70, 13, 2, 43.3, 38.3, '2025-10-20', '2025-10-20'),
(71, 13, 4, 32.9, 29.8, '2025-10-20', '2025-10-20'),
(72, 13, 5, 29.1, 33.8, '2025-10-20', '2025-10-20'),
(73, 13, 7, 49.1, 26.4, '2025-10-20', '2025-10-20'),
(74, 13, 17, 44.4, 30.6, '2025-10-20', '2025-10-20'),
(75, 14, 4, 56.3, 32.7, '2025-10-20', '2025-10-20'),
(76, 14, 7, 47.0, 27.3, '2025-10-20', '2025-10-20'),
(77, 14, 8, 46.5, 26.1, '2025-10-20', '2025-10-20'),
(78, 14, 13, 53.5, 25.1, '2025-10-20', '2025-10-20'),
(79, 14, 18, 42.1, 32.1, '2025-10-20', '2025-10-20'),
(80, 14, 19, 54.6, 28.4, '2025-10-20', '2025-10-20'),
(81, 15, 2, 35.9, 28.5, '2025-10-20', '2025-10-20'),
(82, 15, 5, 52.6, 28.5, '2025-10-20', '2025-10-20'),
(83, 15, 6, 38.4, 39.6, '2025-10-20', '2025-10-20'),
(84, 15, 7, 54.3, 18.9, '2025-10-20', '2025-10-20'),
(85, 15, 8, 55.9, 33.6, '2025-10-20', '2025-10-20'),
(86, 15, 9, 35.7, 32.6, '2025-10-20', '2025-10-20'),
(87, 16, 7, 52.2, 35.5, '2025-10-20', '2025-10-20'),
(88, 16, 10, 44.3, 32.8, '2025-10-20', '2025-10-20'),
(89, 16, 12, 47.1, 38.3, '2025-10-20', '2025-10-20'),
(90, 16, 16, 44.9, 35.2, '2025-10-20', '2025-10-20'),
(91, 16, 17, 47.9, 28.3, '2025-10-20', '2025-10-20'),
(92, 16, 18, 45.6, 35.7, '2025-10-20', '2025-10-20'),
(93, 16, 19, 46.0, 39.4, '2025-10-20', '2025-10-20'),
(94, 17, 2, 54.1, 37.4, '2025-10-20', '2025-10-20'),
(95, 17, 5, 52.6, 31.8, '2025-10-20', '2025-10-20'),
(96, 17, 7, 50.8, 31.1, '2025-10-20', '2025-10-20'),
(97, 17, 13, 54.8, 32.5, '2025-10-20', '2025-10-20'),
(98, 17, 15, 30.4, 16.6, '2025-10-20', '2025-10-20'),
(99, 17, 19, 53.6, 18.0, '2025-10-20', '2025-10-20'),
(100, 18, 2, 59.5, 38.8, '2025-10-20', '2025-10-20');
INSERT INTO `student_management_app_studentresult` (`id`, `student_id_id`, `subject_id_id`, `subject_exam_marks`, `subject_assignment_marks`, `created_at`, `updated_at`) VALUES
(101, 18, 5, 37.4, 28.8, '2025-10-20', '2025-10-20'),
(102, 18, 6, 45.3, 31.0, '2025-10-20', '2025-10-20'),
(103, 18, 16, 32.1, 26.9, '2025-10-20', '2025-10-20'),
(104, 18, 19, 58.0, 38.1, '2025-10-20', '2025-10-20'),
(105, 19, 2, 44.1, 38.3, '2025-10-20', '2025-10-20'),
(106, 19, 4, 55.0, 30.3, '2025-10-20', '2025-10-20'),
(107, 19, 6, 35.5, 26.5, '2025-10-20', '2025-10-20'),
(108, 19, 15, 51.0, 28.2, '2025-10-20', '2025-10-20'),
(109, 19, 17, 43.6, 33.8, '2025-10-20', '2025-10-20'),
(110, 20, 5, 45.6, 33.5, '2025-10-20', '2025-10-20'),
(111, 20, 8, 54.6, 25.4, '2025-10-20', '2025-10-20'),
(112, 20, 10, 40.2, 33.1, '2025-10-20', '2025-10-20'),
(113, 20, 16, 48.1, 37.6, '2025-10-20', '2025-10-20'),
(114, 20, 18, 54.6, 33.4, '2025-10-20', '2025-10-20'),
(115, 21, 5, 35.9, 33.6, '2025-10-20', '2025-10-20'),
(116, 21, 6, 59.3, 25.2, '2025-10-20', '2025-10-20'),
(117, 21, 11, 49.6, 32.8, '2025-10-20', '2025-10-20'),
(118, 21, 12, 23.7, 33.7, '2025-10-20', '2025-10-20'),
(119, 21, 15, 37.4, 30.7, '2025-10-20', '2025-10-20'),
(120, 21, 16, 22.4, 26.6, '2025-10-20', '2025-10-20'),
(121, 22, 1, 41.2, 29.8, '2025-10-20', '2025-10-20'),
(122, 22, 3, 49.5, 38.8, '2025-10-20', '2025-10-20'),
(123, 22, 6, 25.8, 19.0, '2025-10-20', '2025-10-20'),
(124, 22, 11, 48.6, 29.3, '2025-10-20', '2025-10-20'),
(125, 22, 14, 49.5, 28.9, '2025-10-20', '2025-10-20'),
(126, 22, 15, 38.3, 16.7, '2025-10-20', '2025-10-20'),
(127, 22, 19, 42.1, 29.4, '2025-10-20', '2025-10-20'),
(128, 23, 2, 37.3, 34.4, '2025-10-20', '2025-10-20'),
(129, 23, 4, 52.4, 16.4, '2025-10-20', '2025-10-20'),
(130, 23, 5, 24.7, 32.4, '2025-10-20', '2025-10-20'),
(131, 23, 6, 40.0, 37.0, '2025-10-20', '2025-10-20'),
(132, 23, 15, 37.9, 31.0, '2025-10-20', '2025-10-20'),
(133, 23, 18, 40.2, 32.3, '2025-10-20', '2025-10-20'),
(134, 24, 4, 46.7, 37.6, '2025-10-20', '2025-10-20'),
(135, 24, 6, 49.2, 27.2, '2025-10-20', '2025-10-20'),
(136, 24, 8, 38.2, 30.9, '2025-10-20', '2025-10-20'),
(137, 24, 12, 31.8, 27.0, '2025-10-20', '2025-10-20'),
(138, 24, 13, 45.4, 32.4, '2025-10-20', '2025-10-20'),
(139, 24, 18, 40.3, 38.2, '2025-10-20', '2025-10-20'),
(140, 25, 6, 53.7, 20.5, '2025-10-20', '2025-10-20'),
(141, 25, 7, 40.5, 30.7, '2025-10-20', '2025-10-20'),
(142, 25, 10, 51.8, 25.3, '2025-10-20', '2025-10-20'),
(143, 25, 13, 49.4, 26.9, '2025-10-20', '2025-10-20'),
(144, 25, 15, 49.0, 25.3, '2025-10-20', '2025-10-20'),
(145, 25, 16, 47.5, 28.3, '2025-10-20', '2025-10-20'),
(146, 25, 17, 57.5, 29.3, '2025-10-20', '2025-10-20'),
(147, 26, 2, 57.3, 37.6, '2025-10-20', '2025-10-20'),
(148, 26, 4, 42.0, 37.4, '2025-10-20', '2025-10-20'),
(149, 26, 5, 44.3, 39.8, '2025-10-20', '2025-10-20'),
(150, 26, 6, 44.3, 28.4, '2025-10-20', '2025-10-20'),
(151, 26, 7, 37.3, 32.8, '2025-10-20', '2025-10-20'),
(152, 26, 17, 52.8, 39.9, '2025-10-20', '2025-10-20'),
(153, 26, 19, 40.2, 32.2, '2025-10-20', '2025-10-20'),
(154, 27, 1, 45.7, 37.9, '2025-10-20', '2025-10-20'),
(155, 27, 2, 57.8, 37.6, '2025-10-20', '2025-10-20'),
(156, 27, 7, 44.5, 19.3, '2025-10-20', '2025-10-20'),
(157, 27, 8, 40.6, 34.4, '2025-10-20', '2025-10-20'),
(158, 27, 11, 52.6, 28.6, '2025-10-20', '2025-10-20'),
(159, 27, 14, 22.2, 24.9, '2025-10-20', '2025-10-20'),
(160, 27, 18, 43.2, 26.1, '2025-10-20', '2025-10-20'),
(161, 28, 2, 25.7, 33.1, '2025-10-20', '2025-10-20'),
(162, 28, 5, 47.2, 36.3, '2025-10-20', '2025-10-20'),
(163, 28, 11, 45.2, 31.3, '2025-10-20', '2025-10-20'),
(164, 28, 12, 42.9, 35.7, '2025-10-20', '2025-10-20'),
(165, 28, 13, 48.6, 36.5, '2025-10-20', '2025-10-20'),
(166, 28, 16, 58.8, 28.2, '2025-10-20', '2025-10-20'),
(167, 29, 6, 46.4, 31.2, '2025-10-20', '2025-10-20'),
(168, 29, 9, 59.5, 32.8, '2025-10-20', '2025-10-20'),
(169, 29, 10, 37.8, 29.9, '2025-10-20', '2025-10-20'),
(170, 29, 16, 21.1, 21.5, '2025-10-20', '2025-10-20'),
(171, 29, 19, 52.0, 25.6, '2025-10-20', '2025-10-20');
UNLOCK TABLES;


-- Bảng: student_management_app_students
DROP TABLE IF EXISTS `student_management_app_students`;
CREATE TABLE `student_management_app_students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gender` varchar(255) NOT NULL,
  `profile_pic` varchar(100) NOT NULL,
  `address` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `course_id_id` int(11) NOT NULL,
  `session_year_id_id` int(11) NOT NULL,
  `fcm_token` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_id` (`admin_id`),
  KEY `student_management_a_course_id_id_fcd09bed_fk_student_m` (`course_id_id`),
  KEY `student_management_a_session_year_id_id_594fc55d_fk_student_m` (`session_year_id_id`),
  CONSTRAINT `student_management_a_admin_id_1a8517ae_fk_student_m` FOREIGN KEY (`admin_id`) REFERENCES `student_management_app_customuser` (`id`),
  CONSTRAINT `student_management_a_course_id_id_fcd09bed_fk_student_m` FOREIGN KEY (`course_id_id`) REFERENCES `student_management_app_courses` (`id`),
  CONSTRAINT `student_management_a_session_year_id_id_594fc55d_fk_student_m` FOREIGN KEY (`session_year_id_id`) REFERENCES `student_management_app_sessionyearmodel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_students`
LOCK TABLES `student_management_app_students` WRITE;
INSERT INTO `student_management_app_students` (`id`, `gender`, `profile_pic`, `address`, `created_at`, `updated_at`, `admin_id`, `course_id_id`, `session_year_id_id`, `fcm_token`) VALUES
(2, 'Male', '/media/python-student-10_Sa6Q7zb.png', 'Student One Address', '2020-04-12 08:59:08.573132', '2020-04-12 08:59:08.573132', 13, 1, 1, ''),
(3, 'Male', '/media/python-student-10_cv5uwSU.png', 'Staff Two Address Addd', '2020-04-12 09:00:14.779121', '2020-04-12 09:00:14.779121', 14, 1, 1, ''),
(4, 'Male', '', 'Test Address', '2025-10-20 09:22:59.317246', '2025-10-20 09:22:59.317267', 18, 1, 1, ''),
(5, 'Female', '', '258 Cách Mạng Tháng 8, Q10, TP.HCM', '2025-10-20 10:04:24.408159', '2025-10-20 10:04:24.408177', 19, 1, 1, ''),
(6, 'Male', '', '159 Phan Đăng Lưu, Phú Nhuận, TP.HCM', '2025-10-20 10:04:24.667414', '2025-10-20 10:04:24.667426', 20, 1, 1, ''),
(7, 'Female', '', '159 Phan Đăng Lưu, Phú Nhuận, TP.HCM', '2025-10-20 10:04:24.924533', '2025-10-20 10:04:24.924547', 21, 1, 1, ''),
(8, 'Female', '', '654 Võ Văn Tần, Q3, TP.HCM', '2025-10-20 10:04:25.183223', '2025-10-20 10:04:25.183235', 22, 1, 1, ''),
(9, 'Male', '', '123 Lê Lợi, Q1, TP.HCM', '2025-10-20 10:04:25.453165', '2025-10-20 10:04:25.453179', 23, 1, 1, ''),
(10, 'Female', '', '753 Hoàng Văn Thụ, Tân Bình, TP.HCM', '2025-10-20 10:04:25.711012', '2025-10-20 10:04:25.711025', 24, 1, 1, ''),
(11, 'Female', '', '753 Hoàng Văn Thụ, Tân Bình, TP.HCM', '2025-10-20 10:04:25.968028', '2025-10-20 10:04:25.968042', 25, 1, 1, ''),
(12, 'Male', '', '321 Trần Hưng Đạo, Q5, TP.HCM', '2025-10-20 10:04:26.217919', '2025-10-20 10:04:26.217930', 26, 1, 1, ''),
(13, 'Female', '', '147 Điện Biên Phủ, Q10, TP.HCM', '2025-10-20 10:04:26.469301', '2025-10-20 10:04:26.469312', 27, 1, 1, ''),
(14, 'Male', '', '789 Hai Bà Trưng, Q3, TP.HCM', '2025-10-20 10:04:26.713310', '2025-10-20 10:04:26.713324', 28, 1, 1, ''),
(15, 'Male', '', '753 Hoàng Văn Thụ, Tân Bình, TP.HCM', '2025-10-20 10:16:40.533009', '2025-10-20 10:16:40.533021', 29, 1, 1, ''),
(16, 'Male', '', '147 Điện Biên Phủ, Q10, TP.HCM', '2025-10-20 10:16:40.786773', '2025-10-20 10:16:40.786784', 30, 1, 1, ''),
(17, 'Male', '', '123 Lê Lợi, Q1, TP.HCM', '2025-10-20 10:16:41.040674', '2025-10-20 10:16:41.040687', 31, 1, 1, ''),
(18, 'Male', '', '654 Võ Văn Tần, Q3, TP.HCM', '2025-10-20 10:16:41.328338', '2025-10-20 10:16:41.328351', 32, 1, 1, ''),
(19, 'Male', '', '369 Lý Thường Kiệt, Q11, TP.HCM', '2025-10-20 10:16:41.595624', '2025-10-20 10:16:41.595638', 33, 1, 1, ''),
(20, 'Male', '', '456 Nguyễn Huệ, Q1, TP.HCM', '2025-10-20 10:16:41.847179', '2025-10-20 10:16:41.847199', 34, 1, 1, ''),
(21, 'Male', '', '456 Nguyễn Huệ, Q1, TP.HCM', '2025-10-20 10:16:42.112331', '2025-10-20 10:16:42.112344', 35, 1, 1, ''),
(22, 'Male', '', '123 Lê Lợi, Q1, TP.HCM', '2025-10-20 10:16:42.379164', '2025-10-20 10:16:42.379178', 36, 1, 1, ''),
(23, 'Male', '', '456 Nguyễn Huệ, Q1, TP.HCM', '2025-10-20 10:16:42.640423', '2025-10-20 10:16:42.640439', 37, 1, 1, ''),
(24, 'Male', '', '159 Phan Đăng Lưu, Phú Nhuận, TP.HCM', '2025-10-20 10:16:42.912146', '2025-10-20 10:16:42.912158', 38, 1, 1, ''),
(25, 'Female', '', '258 Cách Mạng Tháng 8, Q10, TP.HCM', '2025-10-20 10:16:43.188285', '2025-10-20 10:16:43.188301', 39, 1, 1, ''),
(26, 'Female', '', '456 Nguyễn Huệ, Q1, TP.HCM', '2025-10-20 10:20:57.209168', '2025-10-20 10:20:57.209180', 40, 1, 1, ''),
(27, 'Female', '', '456 Nguyễn Huệ, Q1, TP.HCM', '2025-10-20 10:21:24.764203', '2025-10-20 10:21:24.764216', 41, 1, 1, ''),
(28, 'Male', '', '123 Lê Lợi, Q1, TP.HCM', '2025-10-20 10:21:30.891509', '2025-10-20 10:21:30.891523', 42, 1, 1, ''),
(29, 'Male', '', '456 Nguyễn Huệ, Q1, TP.HCM', '2025-10-20 10:22:27.896044', '2025-10-20 10:22:27.896056', 43, 1, 1, '');
UNLOCK TABLES;


-- Bảng: student_management_app_subjects
DROP TABLE IF EXISTS `student_management_app_subjects`;
CREATE TABLE `student_management_app_subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(255) NOT NULL,
  `subject_code` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id_id` int(11) NOT NULL,
  `staff_id_id` int(11) NOT NULL,
  `credit_hours` int(11) NOT NULL,
  `fee_per_credit` decimal(10,2) NOT NULL,
  `subject_description_file` varchar(100) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `description_file` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_management_a_course_id_id_342668dd_fk_student_m` (`course_id_id`),
  KEY `student_management_a_staff_id_id_5f47119a_fk_student_m` (`staff_id_id`),
  CONSTRAINT `student_management_a_course_id_id_342668dd_fk_student_m` FOREIGN KEY (`course_id_id`) REFERENCES `student_management_app_courses` (`id`),
  CONSTRAINT `student_management_a_staff_id_id_5f47119a_fk_student_m` FOREIGN KEY (`staff_id_id`) REFERENCES `student_management_app_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu cho bảng `student_management_app_subjects`
LOCK TABLES `student_management_app_subjects` WRITE;
INSERT INTO `student_management_app_subjects` (`id`, `subject_name`, `subject_code`, `created_at`, `updated_at`, `course_id_id`, `staff_id_id`, `credit_hours`, `fee_per_credit`, `subject_description_file`, `description`, `description_file`) VALUES
(1, 'Java', 'MH_1', '2020-04-12 08:39:32.320256', '2020-04-12 08:39:32.320256', 1, 2, 3, '500000.00', '', NULL, ''),
(2, 'PHP', 'MH_2', '2020-04-12 08:39:36.671226', '2020-04-12 08:39:36.671226', 1, 2, 3, '500000.00', '', NULL, ''),
(3, 'MySql', 'MH_3', '2020-04-12 08:39:45.961429', '2020-04-12 08:39:45.961429', 1, 2, 3, '500000.00', '', NULL, ''),
(4, 'HTML', 'MH_4', '2020-04-12 08:39:51.772865', '2020-04-12 08:39:51.772865', 1, 2, 3, '500000.00', '', NULL, ''),
(5, 'Accounts', 'MH_5', '2020-04-12 08:40:01.554850', '2020-04-12 08:40:01.554850', 2, 3, 3, '500000.00', '', NULL, ''),
(6, 'Marketing', 'MH_6', '2020-04-12 08:40:16.095706', '2020-04-12 08:40:16.095706', 2, 3, 3, '500000.00', '', NULL, ''),
(7, 'ETP', 'MH_7', '2020-04-12 08:40:27.113388', '2020-04-12 08:40:27.113388', 2, 3, 3, '500000.00', '', NULL, ''),
(8, 'Math', 'MH_8', '2020-04-12 08:40:39.975428', '2020-04-12 08:40:39.975428', 4, 4, 3, '500000.00', '', NULL, ''),
(9, 'Python', 'MH_9', '2020-04-12 08:40:48.928138', '2020-04-12 08:40:48.928138', 4, 4, 3, '500000.00', '', NULL, ''),
(10, 'Machine Learning', 'MA_LEARNI', '2020-04-12 08:40:57.217406', '2020-04-12 08:40:57.217406', 4, 4, 3, '500000.00', '', NULL, ''),
(11, 'Artifical Intelligence', 'AR_INTELL', '2020-04-12 08:41:11.197563', '2020-04-12 08:41:11.197563', 4, 4, 3, '500000.00', '', NULL, ''),
(12, 'Cost Accounting', 'CO_ACCOUN', '2020-04-12 08:41:20.505769', '2020-04-12 08:41:20.505769', 3, 5, 3, '500000.00', '', NULL, ''),
(13, 'Financial Accounting', 'FI_ACCOUN', '2020-04-12 08:41:29.711299', '2020-04-12 08:41:29.711299', 3, 5, 3, '500000.00', '', NULL, ''),
(14, 'Statistics', 'MH_14', '2020-04-12 08:41:49.726616', '2020-04-12 08:41:49.726616', 3, 5, 3, '500000.00', '', NULL, ''),
(15, 'Lập trình Python nâng cao', 'LẬ_TRÌNH', '2025-10-20 09:53:10.589819', '2025-10-20 09:53:10.589847', 1, 2, 4, '500000.00', '', NULL, ''),
(16, 'Cơ sở dữ liệu Oracle', 'CƠ_SỞ', '2025-10-20 09:53:10.606646', '2025-10-20 09:53:10.606667', 1, 2, 3, '500000.00', '', NULL, ''),
(17, 'Phát triển Web với Django', 'PH_TRIỂN', '2025-10-20 09:53:10.609656', '2025-10-20 09:53:10.609681', 1, 2, 4, '500000.00', '', NULL, ''),
(18, 'Trí tuệ nhân tạo ứng dụng', 'TR_TUỆ', '2025-10-20 09:53:10.612764', '2025-10-20 09:53:10.612782', 1, 2, 3, '500000.00', '', NULL, ''),
(19, 'An ninh mạng', 'AN_NINH', '2025-10-20 09:53:10.615643', '2025-10-20 09:53:10.615670', 1, 2, 3, '500000.00', '', NULL, '');
UNLOCK TABLES;


SET FOREIGN_KEY_CHECKS=1;
COMMIT;
