<?php

function theme_setup() {
    // Add WooCommerce support
    add_theme_support( 'woocommerce' );

    // Add other theme supports as before
    add_theme_support( 'title-tag' );

    // Rest of your existing theme setup code...
}

add_action( 'after_setup_theme', 'theme_setup' );


function register_custom_api_endpoints() {
    // Register a REST route
    register_rest_route('wp/v2', '/settings', array(
        'methods'  => 'GET',
        'callback' => 'get_custom_settings',
        'permission_callback' => '__return_true' // Make it publicly accessible
    ));
}

add_action('rest_api_init', 'register_custom_api_endpoints');

function get_custom_settings() {
    // Fetch settings data
    $settings = array(
        'title'             => get_bloginfo('name'),
        'description'       => get_bloginfo('description'),
        'logo'              => wp_get_attachment_image_url( get_theme_mod( 'custom_logo' ), 'full' ), // Fetch logo URL
        'header_image'      => get_header_image(), // Fetch header image URL
        'posts_per_page'    => get_option('posts_per_page', 10), // Retrieve the number of posts per page setting
    );

    return new WP_REST_Response($settings, 200);
}