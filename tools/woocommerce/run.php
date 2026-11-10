<?php
/**
 * Nhập dữ liệu mẫu SANCTUARY vào WooCommerce (bản cài thử trên WordPress Playground).
 * Mở http://127.0.0.1:9400/sanctuary-seed/run.php sau khi server chạy (xem README.md cùng thư mục).
 * Chỉ dùng trên máy cá nhân để làm đồ án: file này không kiểm tra quyền, KHÔNG đưa lên host thật.
 *
 * Việc script làm (tương ứng mục 7.4.3 và 7.4.4 trong đề cương):
 *   1. Tạo danh mục sản phẩm, thuộc tính Size, 12 sản phẩm có biến thể theo size, ảnh, tồn kho
 *   2. Tạo 3 khách hàng có địa chỉ
 *   3. Tạo 6 đơn hàng với nhiều trạng thái khác nhau
 *   4. Cấu hình vùng giao hàng và thuế VAT Việt Nam
 *   5. Tùy biến giao diện Storefront sang tông đen trắng của SANCTUARY
 */
require_once dirname(__DIR__) . '/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
header('Content-Type: text/plain; charset=utf-8');

if (get_option('sanctuary_seeded')) { exit("Đã nhập dữ liệu rồi.\n"); }
wp_set_current_user(1);
$dir  = __DIR__ . '/seed';
$data = json_decode(file_get_contents($dir . '/seed.json'), true);

// Tải 1 file ảnh từ thư mục seed vào Thư viện Media, trả về ID ảnh
function sanctuary_media($path, $title) {
    $tmp = wp_tempnam(basename($path));
    copy($path, $tmp);
    $id = media_handle_sideload(['name' => basename($path), 'tmp_name' => $tmp], 0, $title);
    return is_wp_error($id) ? 0 : $id;
}

// Lấy (hoặc tạo) danh mục, có thể nằm trong danh mục cha
function sanctuary_term($name, $parent = 0) {
    $t = term_exists($name, 'product_cat', $parent);
    if (!$t) { $t = wp_insert_term($name, 'product_cat', ['parent' => $parent]); }
    return (int) $t['term_id'];
}

// ---- 1. Thuộc tính toàn cục "Size" ----
if (!wc_attribute_taxonomy_id_by_name('size')) {
    wc_create_attribute(['name' => 'Size', 'slug' => 'size', 'type' => 'select', 'order_by' => 'menu_order']);
    register_taxonomy('pa_size', ['product']);
}
foreach (['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'One Size'] as $s) {
    if (!term_exists($s, 'pa_size')) { wp_insert_term($s, 'pa_size'); }
}

// ---- 1. Sản phẩm có biến thể theo size ----
$product_ids = [];
foreach ($data['products'] as $i => $p) {
    $line = sanctuary_term($p['line']);
    $cat  = sanctuary_term($p['category'], $line);

    $prod = new WC_Product_Variable();
    $prod->set_name($p['name']);
    $prod->set_sku($p['sku']);
    $prod->set_description($p['description']);
    $prod->set_short_description($p['short'] . ' Colors: ' . implode(', ', $p['colors']) . '.');
    $prod->set_category_ids([$line, $cat]);
    $prod->set_featured($i < 4);
    $prod->set_manage_stock(true);              // quản lý tồn kho ở cấp sản phẩm cha
    $prod->set_stock_quantity($p['stock']);
    $prod->set_image_id(sanctuary_media($dir . '/img/' . $p['image'], $p['name']));

    $sizes = $p['sizes'] ?: ['One Size'];
    $attr = new WC_Product_Attribute();
    $attr->set_id(wc_attribute_taxonomy_id_by_name('size'));
    $attr->set_name('pa_size');
    $attr->set_options(array_map(fn($s) => get_term_by('name', $s, 'pa_size')->term_id, $sizes));
    $attr->set_visible(true);
    $attr->set_variation(true);
    $prod->set_attributes([$attr]);
    $pid = $prod->save();

    foreach ($sizes as $s) {                    // mỗi size là 1 biến thể cùng giá
        $v = new WC_Product_Variation();
        $v->set_parent_id($pid);
        $v->set_attributes(['pa_size' => get_term_by('name', $s, 'pa_size')->slug]);
        $v->set_regular_price((string) $p['price']);
        $v->save();
    }
    WC_Product_Variable::sync($pid);
    $product_ids[] = $pid;
    echo "Sản phẩm: {$p['name']}\n";
}

// ---- 2. Khách hàng (trùng dữ liệu mẫu trong trang admin của web) ----
$customers = [
    ['Minh', 'Tran', 'minh.tran@example.com', '0903 456 789', '45 Le Loi Street', 'Ho Chi Minh City', 'VN'],
    ['Jordan', 'Reyes', 'jordan.reyes@example.com', '+1 415 555 0142', '820 Mission Street', 'San Francisco', 'US'],
    ['Hana', 'Sato', 'hana.sato@example.com', '+81 90 1234 5678', '2-11-3 Shibuya', 'Tokyo', 'JP'],
];
$customer_ids = [];
foreach ($customers as $c) {
    $uid = email_exists($c[2]) ?: wc_create_new_customer($c[2], '', 'Sanctuary1');
    $cu = new WC_Customer($uid);
    $cu->set_first_name($c[0]); $cu->set_last_name($c[1]);
    foreach (['billing', 'shipping'] as $type) {
        $cu->{"set_{$type}_first_name"}($c[0]); $cu->{"set_{$type}_last_name"}($c[1]);
        $cu->{"set_{$type}_address_1"}($c[4]); $cu->{"set_{$type}_city"}($c[5]); $cu->{"set_{$type}_country"}($c[6]);
    }
    $cu->set_billing_email($c[2]); $cu->set_billing_phone($c[3]);
    $cu->save();
    $customer_ids[] = $uid;
    echo "Khách: {$c[0]} {$c[1]}\n";
}

// ---- 4. Vùng giao hàng + thuế (đặt trước khi tạo đơn để đơn có phí ship) ----
$zone = new WC_Shipping_Zone();
$zone->set_zone_name('Vietnam');
$zone->add_location('VN', 'country');
$zone->save();
$iid = $zone->add_shipping_method('flat_rate');
update_option('woocommerce_flat_rate_' . $iid . '_settings', ['title' => 'Standard (2-4 days)', 'cost' => '3', 'tax_status' => 'taxable']);
$intl = new WC_Shipping_Zone();
$intl->set_zone_name('International');
foreach (['US', 'JP', 'KR', 'SG', 'AU', 'GB'] as $cc) { $intl->add_location($cc, 'country'); }
$intl->save();
$iid2 = $intl->add_shipping_method('flat_rate');
update_option('woocommerce_flat_rate_' . $iid2 . '_settings', ['title' => 'International express', 'cost' => '24', 'tax_status' => 'none']);
WC_Tax::_insert_tax_rate(['tax_rate_country' => 'VN', 'tax_rate' => '8.0000', 'tax_rate_name' => 'VAT', 'tax_rate_priority' => 1, 'tax_rate_shipping' => 1, 'tax_rate_order' => 0, 'tax_rate_class' => '']);

// ---- 3. Đơn hàng: [khách, [chỉ số sản phẩm, số lượng]..., trạng thái, số ngày trước] ----
$orders = [
    [0, [[0, 1], [7, 1]], 'completed', 9],
    [1, [[5, 1]], 'completed', 7],
    [2, [[8, 1], [9, 2]], 'processing', 4],
    [0, [[4, 1]], 'processing', 2],
    [1, [[1, 2], [2, 1]], 'on-hold', 1],
    [2, [[10, 1]], 'cancelled', 1],
];
foreach ($orders as $o) {
    $cu = new WC_Customer($customer_ids[$o[0]]);
    $order = wc_create_order(['customer_id' => $customer_ids[$o[0]]]);
    foreach ($o[1] as [$idx, $qty]) {
        $parent = wc_get_product($product_ids[$idx]);
        $children = $parent->get_children();
        $order->add_product(wc_get_product($children[min(3, count($children) - 1)]), $qty);   // size M (hoặc One Size)
    }
    $order->set_address($cu->get_billing(), 'billing');
    $order->set_address($cu->get_shipping(), 'shipping');
    $ship = new WC_Order_Item_Shipping();
    $ship->set_method_title($cu->get_shipping_country() === 'VN' ? 'Standard (2-4 days)' : 'International express');
    $ship->set_method_id('flat_rate');
    $ship->set_total($cu->get_shipping_country() === 'VN' ? 3 : 24);
    $order->add_item($ship);
    $order->set_payment_method_title('Credit card (demo)');
    $order->calculate_totals();
    $order->set_date_created(time() - $o[3] * DAY_IN_SECONDS);
    $order->update_status($o[2], 'Sample order for the student project.');
    if ($o[2] !== 'cancelled') { wc_reduce_stock_levels($order->get_id()); }
    echo "Đơn #{$order->get_id()}: {$o[2]}\n";
}

// ---- 5. Tùy biến giao diện Storefront: tông đen trắng như web SANCTUARY ----
$logo = sanctuary_media($dir . '/img/logo.png', 'SANCTUARY logo');
set_theme_mod('custom_logo', $logo);
$mods = [
    'storefront_header_background_color' => '#000000', 'storefront_header_text_color' => '#bbbbbb',
    'storefront_header_link_color' => '#ffffff', 'background_color' => '0a0a0a',
    'storefront_heading_color' => '#ffffff', 'storefront_text_color' => '#d6d6d6',
    'storefront_accent_color' => '#ffffff', 'storefront_hero_heading_color' => '#ffffff',
    'storefront_footer_background_color' => '#000000', 'storefront_footer_heading_color' => '#ffffff',
    'storefront_footer_text_color' => '#8a8a8a', 'storefront_footer_link_color' => '#ffffff',
    'storefront_button_background_color' => '#ffffff', 'storefront_button_text_color' => '#000000',
    'storefront_button_alt_background_color' => '#cc0000', 'storefront_button_alt_text_color' => '#ffffff',
];
foreach ($mods as $k => $v) { set_theme_mod($k, $v); }

update_option('sanctuary_seeded', 1);
echo "Xong.\n";
