--
-- Database: `lead_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `assigned_leads`
--

CREATE TABLE `assigned_leads` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `prob` float default NULL,
  `risk` varchar(50) default NULL,
  `summary` text,
  `action` text,
  `assigned_by` varchar(50) default NULL,
  `assigned_to` varchar(100) default NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `phone` varchar(15) default NULL,
  `status` varchar(50) default 'Pending',
  `call_count` int(11) default '0',
  `updated_by` varchar(100) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `assigned_leads`
--

INSERT INTO `assigned_leads` (`id`, `name`, `prob`, `risk`, `summary`, `action`, `assigned_by`, `assigned_to`, `created_at`, `phone`, `status`, `call_count`, `updated_by`) VALUES
(1, 'Amit Sharma', 99.72, 'High Potential', 'Amit Sharma shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543210', 'Not Interested', 1, 'raj'),
(2, 'Priya Nair', 95.22, 'High Potential', 'Priya Nair shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543211', 'Joined', 2, 'raj'),
(3, 'Divya Iyer', 100, 'High Potential', 'Divya Iyer shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543213', 'Interested', 1, 'raj'),
(4, 'Kavya Reddy', 100, 'High Potential', 'Kavya Reddy shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543215', 'Pending', 0, NULL),
(5, 'Meena Krishnan', 89.29, 'High Potential', 'Meena Krishnan shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543217', 'Pending', 0, NULL),
(6, 'Rohit Verma', 99, 'High Potential', 'Rohit Verma shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543218', 'Pending', 0, NULL),
(7, 'Vikram Rao', 99.5, 'High Potential', 'Vikram Rao shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543220', 'Pending', 0, NULL),
(8, 'Aishwarya Das', 98.95, 'High Potential', 'Aishwarya Das shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543221', 'Pending', 0, NULL),
(9, 'Nisha Menon', 100, 'High Potential', 'Nisha Menon shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543223', 'Pending', 0, NULL),
(10, 'Karthik Subramani', 100, 'High Potential', 'Karthik Subramani shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543224', 'Pending', 0, NULL),
(11, 'Neha Singh', 96.15, 'High Potential', 'Neha Singh shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543225', 'Pending', 0, NULL),
(12, 'Anjali Sharma', 87, 'High Potential', 'Anjali Sharma shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543227', 'Pending', 0, NULL),
(13, 'Deepak Yadav', 99.5, 'High Potential', 'Deepak Yadav shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543228', 'Pending', 0, NULL),
(14, 'Pooja Kulkarni', 98.5, 'High Potential', 'Pooja Kulkarni shows strong interest based on engagement.', 'Follow immediately', 'raj', 'raj', '2026-04-16 14:27:26', '9876543229', 'Pending', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `course_bookings`
--

CREATE TABLE `course_bookings` (
  `id` int(11) NOT NULL auto_increment,
  `full_name` varchar(100) default NULL,
  `age` int(11) default NULL,
  `gender` varchar(20) default NULL,
  `location` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `phone` varchar(20) default NULL,
  `education` varchar(20) default NULL,
  `occupation` varchar(20) default NULL,
  `experience_years` int(11) default NULL,
  `course_interest` varchar(50) default NULL,
  `budget` int(11) default NULL,
  `payment_mode` varchar(20) default NULL,
  `preferred_time` varchar(50) default NULL,
  `device_type` varchar(20) default NULL,
  `time_spent` int(11) default NULL,
  `pages_visited` int(11) default NULL,
  `click_count` int(11) default NULL,
  `previous_enquiry` varchar(10) default NULL,
  `demo_attended` varchar(10) default NULL,
  `webinar_attended` varchar(10) default NULL,
  `source` varchar(50) default NULL,
  `email_opened` varchar(10) default NULL,
  `email_clicked` varchar(10) default NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `course_bookings`
--


-- --------------------------------------------------------

--
-- Table structure for table `leads`
--

CREATE TABLE `leads` (
  `id` int(11) NOT NULL auto_increment,
  `student_id` int(11) default NULL,
  `course_interest` varchar(100) default NULL,
  `budget` int(11) default NULL,
  `status` varchar(50) default NULL,
  PRIMARY KEY  (`id`),
  KEY `student_id` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `leads`
--


-- --------------------------------------------------------

--
-- Table structure for table `marketing_manager`
--

CREATE TABLE `marketing_manager` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(15) default NULL,
  `company_name` varchar(100) default NULL,
  `location` varchar(100) default NULL,
  `company_type` varchar(100) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `marketing_manager`
--

INSERT INTO `marketing_manager` (`id`, `name`, `email`, `mobile`, `company_name`, `location`, `company_type`, `username`, `password`) VALUES
(1, 'Raj', 'raj@gmail.com', '8929090909', 'TCS', 'Chathiram', 'IT', 'raj', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(15) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `name`, `email`, `mobile`, `username`, `password`) VALUES
(1, 'Raj', 'raj@gmail.com', '8929090909', 'raj', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `telecaller`
--

CREATE TABLE `telecaller` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(15) default NULL,
  `working_type` varchar(50) default NULL,
  `working_time` varchar(50) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `telecaller`
--

INSERT INTO `telecaller` (`id`, `name`, `email`, `mobile`, `working_type`, `working_time`, `username`, `password`) VALUES
(1, 'Raj', 'projectbased2k26@gmail.com', '8929090909', 'Full-Time', '9AM - 9PM', 'raj', '1234');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `leads`
--
ALTER TABLE `leads`
  ADD CONSTRAINT `leads_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);
