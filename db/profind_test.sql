-- phpMyAdmin SQL Dump
-- version 4.4.3
-- http://www.phpmyadmin.net
--
-- Anamakine: localhost
-- Üretim Zamanı: 24 May 2018, 05:45:46
-- Sunucu sürümü: 5.6.24
-- PHP Sürümü: 5.6.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Veritabanı: `profind_test`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `id` int(10) unsigned NOT NULL,
  `category_id` int(10) unsigned NOT NULL DEFAULT '0',
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `alias` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `categories`
--

INSERT INTO `categories` (`id`, `category_id`, `name`, `alias`) VALUES
(1, 0, 'Electronic', 'electronic'),
(2, 1, 'Computer & Tablet', 'computer'),
(3, 1, 'Printer & Projector', 'printer'),
(4, 1, 'Phone & Phone Accessories', 'phone'),
(5, 1, 'Television', 'television'),
(6, 1, 'White Goods', 'white_goods'),
(7, 1, 'Camera', 'camera'),
(8, 1, 'Air Conditioning', 'air_conditioning'),
(9, 1, 'Game & Game Consoles', 'game'),
(10, 0, 'Women''s Clothing & Fashion', 'women'),
(11, 10, 'Clothing', 'clothing'),
(12, 10, 'Shoes', 'shoes'),
(13, 10, 'Bags & Suitcases', 'bags'),
(14, 10, 'Accessories', 'accessories'),
(15, 0, 'Men''s Clothing & Fashion', 'men'),
(16, 15, 'Clothing', 'clothing'),
(17, 15, 'Shoes', 'shoes'),
(18, 15, 'Bags & Suitcases', 'bags'),
(19, 15, 'Accessories', 'accessories'),
(20, 0, 'Books & Magazines', 'books'),
(21, 0, 'Sport & Outdoor', 'sport'),
(22, 21, 'Bicycle', 'bicycle'),
(23, 21, 'Fitness & Pilates', 'fitness'),
(24, 21, 'Inflatable Water Products', 'water'),
(25, 21, 'Hunting Equipment', 'hunting'),
(26, 0, 'Cosmetic', 'cosmetic'),
(27, 0, 'Home & Life', 'home'),
(28, 27, 'Furniture', 'furniture'),
(29, 27, 'Home textiles', 'textiles'),
(30, 27, 'Decoration', 'decoration'),
(31, 27, 'Bathroom', 'bathroom'),
(32, 0, 'Baby', 'baby'),
(33, 32, 'Toys', 'toys'),
(34, 32, 'Clothing & Shoes', 'girls'),
(36, 32, 'Accessories', 'accessories'),
(37, 0, 'Office Products', 'office'),
(38, 37, 'Stationery', 'stationery'),
(39, 37, 'Furnitures & Accessories', 'furnitures'),
(40, 0, 'Pet Supplies', 'pet');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `ecommerce_sites`
--

CREATE TABLE IF NOT EXISTS `ecommerce_sites` (
  `id` int(10) unsigned NOT NULL,
  `name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `ecommerce_sites`
--

INSERT INTO `ecommerce_sites` (`id`, `name`, `url`) VALUES
(1, 'Hepsiburada', 'http://www.hepsiburada.com'),
(2, 'Trendyol', 'http://trendyol.com'),
(3, 'Markafoni', 'http://markafoni.com');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `products`
--

CREATE TABLE IF NOT EXISTS `products` (
  `id` bigint(20) unsigned NOT NULL,
  `ecommerce_site_id` int(10) unsigned NOT NULL,
  `category_id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `old_price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `discount` float NOT NULL DEFAULT '0',
  `currency` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `link` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `ecommerce_sites`
--
ALTER TABLE `ecommerce_sites`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(10) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=41;
--
-- Tablo için AUTO_INCREMENT değeri `ecommerce_sites`
--
ALTER TABLE `ecommerce_sites`
  MODIFY `id` int(10) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- Tablo için AUTO_INCREMENT değeri `products`
--
ALTER TABLE `products`
  MODIFY `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
