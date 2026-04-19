-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 05, 2025 at 11:34 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(300) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`, `created_at`) VALUES
(1, 'admin@example.com', '$2b$12$k24Ba3qxyxfJVX7iWoeUkua/RlPp9mRpv56hkMxdDhiIXzdspw1L.', '2025-11-26 19:26:12');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(9, 'Computers'),
(8, 'Laptops'),
(12, 'Networking'),
(13, 'Power'),
(10, 'Printers'),
(11, 'Storage');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `shipping_address` text DEFAULT NULL,
  `shipping_name` varchar(200) DEFAULT NULL,
  `shipping_phone` varchar(50) DEFAULT NULL,
  `order_number` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `total`, `payment_method`, `status`, `shipping_address`, `shipping_name`, `shipping_phone`, `order_number`, `created_at`) VALUES
(1, 1, '212400.00', 'Mobile Money', 'Pending', 'kigali', 'prince6', '0791756870', 'ORD-20251126-47SPYV', '2025-11-26 20:21:38'),
(2, 2, '1180000.00', 'Mobile Money', 'Pending', 'muhanga', 'Cyusaprince1\'s Org', '0791756870', 'ORD-20251204-4XKOZY', '2025-12-04 12:35:06'),
(3, 2, '1180000.00', 'Mobile Money', 'Pending', 'muhanga', 'Cyusaprince1\'s Org', '0791756870', 'ORD-20251204-JQLWF4', '2025-12-04 18:31:18'),
(4, 3, '826000.00', 'Mobile Money', 'Pending', 'muhanga', 'isaro', '0791756870', 'ORD-20251205-EE0TXH', '2025-12-05 08:16:17'),
(5, 3, '944000.00', 'Cash on Delivery', 'Pending', 'muhanga', 'isaro', '0791756870', 'ORD-20251205-3EDI41', '2025-12-05 08:53:23'),
(6, 3, '590000.00', 'Cash on Delivery', 'Pending', 'muhanga', 'isaro', '0791756870', 'ORD-20251205-PTO73O', '2025-12-05 08:56:26'),
(7, 3, '786500.00', 'Mobile Money', 'Pending', 'muhanga', 'isaro', '0791756870', 'ORD-20251205-YHODMB', '2025-12-05 10:32:34');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `price`) VALUES
(2, 2, 2, 2, '500000.00'),
(3, 3, 2, 2, '500000.00'),
(4, 4, 8, 1, '700000.00'),
(5, 5, 3, 2, '400000.00'),
(6, 6, 2, 1, '500000.00'),
(7, 7, 9, 1, '85000.00'),
(8, 7, 8, 1, '700000.00');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `trending` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `price`, `description`, `category_id`, `image`, `stock`, `trending`, `created_at`) VALUES
(2, 'HP EliteBook 840 G5 i7', '500000.00', 'Professional business laptop with Intel Core i7 processor, premium build quality. Perfect for demanding business applications and multitasking.', 8, 'products/EliteBook 840 G5 i7 ; 500,000 RWF.jpg', 5, 0, '2025-12-04 12:23:10'),
(3, 'HP EliteBook 830 i5', '400000.00', 'Compact business laptop with Intel Core i5, perfect for professionals on the go. Lightweight design with excellent performance.', 8, 'products/HP EliteBook 830 i5 ; 400,000 RWF.jpg', 6, 0, '2025-12-04 12:23:10'),
(4, 'HP Envy X360 i7', '1200000.00', '2-in-1 convertible laptop with Intel Core i7, touchscreen display, versatile design. Transform from laptop to tablet mode effortlessly.', 8, 'products/Hp envy X360 i7 ; 1,200,000 RWF.jpeg', 5, 0, '2025-12-04 12:23:10'),
(5, 'HP 290 Desktop', '850000.00', 'Compact desktop computer, ideal for office and home use. Reliable performance for everyday computing tasks.', 9, 'products/HP-290 ; 850,000 RWF.jpg', 7, 0, '2025-12-04 12:23:10'),
(6, 'EPSON L3250', '280000.00', 'EcoTank all-in-one printer with wireless connectivity, high-capacity ink tanks. Print, scan, and copy with cost-effective ink system.', 10, 'products/EPSON L3250 ; 280,000 RWF.jpg', 12, 0, '2025-12-04 12:23:10'),
(7, 'Epson L3210', '250000.00', 'EcoTank printer with refillable ink system, cost-effective printing solution. Save money with refillable ink tanks.', 10, 'products/Epson-L3210 ; 250,000 RWF.png', 15, 0, '2025-12-04 12:23:10'),
(8, 'Canon ImageRunner 2224if', '700000.00', 'Multifunction printer with copy, scan, fax capabilities, network ready. Perfect for small to medium offices.', 10, 'products/imagerunner-2224if ; 700,000 Rwf.avif', 4, 0, '2025-12-04 12:23:10'),
(9, 'XPRINTER 80', '85000.00', 'Compact thermal printer, perfect for receipts and labels. Ideal for retail and small businesses.', 10, 'products/XPRINTER 80 ; 85,000 RWF.jpg', 19, 0, '2025-12-04 12:23:10'),
(10, 'SSD 512GB', '55000.00', 'High-speed 512GB solid state drive, upgrade your computer\'s performance. Dramatically faster than traditional hard drives.', 11, 'products/SSD 512 ; 55,000 RWF.jpeg', 25, 0, '2025-12-04 12:23:10'),
(11, 'Flash Drive 64GB', '20000.00', 'Portable USB flash drive with 64GB storage capacity. Perfect for transferring files and backing up data.', 11, 'products/FLASH 64G ; 20,000 RWF.webp', 30, 0, '2025-12-04 12:23:10'),
(12, 'CAT6 SFTP Cable', '110000.00', 'Shielded twisted pair network cable, high-speed data transmission. Perfect for reliable network connections.', 12, 'products/CAT6-SFTP ; 110,000 RWF.avif', 18, 0, '2025-12-04 12:23:10'),
(13, 'UTP CAT6 Cable', '65000.00', 'Unshielded twisted pair network cable, reliable Ethernet connection. Standard network cable for home and office.', 12, 'products/UTP CAT6 ; 65,000 RWF.jpg', 22, 0, '2025-12-04 12:23:10'),
(14, 'APC SMART UPS 750V', '900000.00', 'Uninterruptible power supply with 750VA capacity, protects your equipment from power surges and outages.', 13, 'products/APC SMART 750V ; 900,000 RWF', 4, 0, '2025-12-04 12:23:10');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` >= 1 and `rating` <= 5),
  `comment` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `site_settings`
--

CREATE TABLE `site_settings` (
  `id` int(11) NOT NULL,
  `setting_key` varchar(100) NOT NULL,
  `setting_value` text DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `site_settings`
--

INSERT INTO `site_settings` (`id`, `setting_key`, `setting_value`, `updated_at`) VALUES
(2, 'home_video', 'WhatsApp_Video_2025-12-03_at_16.12.29_1764856399.mp4', '2025-12-04 13:53:19');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `password` varchar(300) NOT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `phone`, `password`, `address`, `created_at`) VALUES
(1, 'prince6', 'princecyusa6@gmail.com', '0791756870', '$2b$12$uVhCSunM3bunzriJ/NtJmeEFUjK0z3wrDV7FAxYYNcUbonKDDoCPC', '', '2025-11-26 19:48:16'),
(2, 'Cyusaprince1\'s Org', 'admin@example.com', '0791756870', '$2b$12$.EdqHaiWF9v2hJExWXCZaugiC3GB4bJrIcvZoyZae6pYXglQbf0vq', 'muhanga', '2025-12-04 12:34:00'),
(3, 'isaro', 'uwinezaisaro@gmail.com', '0791756870', '$2b$12$o5RZWQh639YBZWkPp.B1Aelx.Kk7oBWKVl3As60dSjYOX.mS0zkJG', 'muhanga', '2025-12-05 08:13:51');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_cart_item` (`user_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_review` (`product_id`,`user_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `site_settings`
--
ALTER TABLE `site_settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `setting_key` (`setting_key`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `site_settings`
--
ALTER TABLE `site_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
