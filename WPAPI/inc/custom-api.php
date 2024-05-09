<?php



// Callback function to retrieve post by slug
function get_post_by_slug_callback( $request ) {
    $slug = $request['slug'];

    // Query the post by its slug
    $post = get_page_by_path( $slug, OBJECT, 'post' );

    if ( ! $post ) {
        return new WP_Error( 'post_not_found', 'Post not found', array( 'status' => 404 ) );
    }

    // Get author data
    $author = get_userdata($post->post_author);

    // Get post data
    $post_data = array(
        'id'             => $post->ID,
        'title'          => get_the_title($post->ID),
        'content'        => apply_filters('the_content', $post->post_content),
        'date'           => get_the_date('c', $post),  // ISO 8601 format
        'author'         => array(
            'id'            => $author->ID,
            'name'          => $author->display_name,
            'url'           => get_author_posts_url($author->ID),
        ),
        'categories'     => wp_get_post_categories($post->ID, array('fields' => 'names')),
        'tags'           => wp_get_post_terms($post->ID, 'post_tag', array('fields' => 'names')),
    );

    // Check if there's a featured image associated with the post
    if (has_post_thumbnail($post->ID)) {
        $image_id = get_post_thumbnail_id($post->ID);
        $image_url = wp_get_attachment_image_url($image_id, 'full');  // Change 'full' to another size if necessary
        $post_data['featured_image'] = $image_url;
    } else {
        $post_data['featured_image'] = null;  // Or specify a default image URL
    }

    // Return post data
    return rest_ensure_response($post_data);
}

// Register custom REST API endpoint
function register_post_by_slug_endpoint() {
    register_rest_route( 'custom/v1', '/post-by-slug/(?P<slug>[a-zA-Z0-9-]+)', array(
        'methods'             => 'GET',
        'callback'            => 'get_post_by_slug_callback',
        'permission_callback' => '__return_true', // Adjust permissions as needed
    ) );
}

add_action( 'rest_api_init', 'register_post_by_slug_endpoint' );

//  ____                   _         _                     _   _                     
// |  _ \    ___    __ _  (_)  ___  | |_    ___   _ __    | | | |  ___    ___   _ __ 
// | |_) |  / _ \  / _` | | | / __| | __|  / _ \ | '__|   | | | | / __|  / _ \ | '__|
// |  _ <  |  __/ | (_| | | | \__ \ | |_  |  __/ | |      | |_| | \__ \ |  __/ | |   
// |_| \_\  \___|  \__, | |_| |___/  \__|  \___| |_|       \___/  |___/  \___| |_|   
//                 |___/                                                             


// Add a custom endpoint for user registration
function custom_register_user_route() {
    register_rest_route( 'custom/v1', '/register', array(
        'methods' => 'POST',
        'callback' => 'custom_register_user',
    ));
}
add_action( 'rest_api_init', 'custom_register_user_route' );

// Custom function to handle user registration
function custom_register_user( $data ) {
    $username = sanitize_text_field( $data['username'] );
    $email = sanitize_email( $data['email'] );
    $password = $data['password'];

    $user_id = wp_create_user( $username, $password, $email );

    if ( is_wp_error( $user_id ) ) {
        return new WP_Error( 'registration_error', $user_id->get_error_message(), array( 'status' => 400 ) );
    }

    // You can perform additional actions here like sending a confirmation email, etc.

    return array( 'message' => 'User registered successfully', 'user_id' => $user_id );
}

//  _____                                  _       ____                                                      _     _____                       _   _     ____                       _ 
// |  ___|   ___    _ __    __ _    ___   | |_    |  _ \    __ _   ___   ___  __      __   ___    _ __    __| |   | ____|  _ __ ___     __ _  (_) | |   / ___|    ___   _ __     __| |
// | |_     / _ \  | '__|  / _` |  / _ \  | __|   | |_) |  / _` | / __| / __| \ \ /\ / /  / _ \  | '__|  / _` |   |  _|   | '_ ` _ \   / _` | | | | |   \___ \   / _ \ | '_ \   / _` |
// |  _|   | (_) | | |    | (_| | | (_) | | |_    |  __/  | (_| | \__ \ \__ \  \ V  V /  | (_) | | |    | (_| |   | |___  | | | | | | | (_| | | | | |    ___) | |  __/ | | | | | (_| |
// |_|      \___/  |_|     \__, |  \___/   \__|   |_|      \__,_| |___/ |___/   \_/\_/    \___/  |_|     \__,_|   |_____| |_| |_| |_|  \__,_| |_| |_|   |____/   \___| |_| |_|  \__,_|
//                         |___/                                                                                                                                                      
// Step 1: Install and activate the WP Mail SMTP plugin


// Add custom endpoint for forgot password
function custom_forgot_password_route() {
    register_rest_route( 'custom/v1', '/forgot-password', array(
        'methods' => 'POST',
        'callback' => 'custom_forgot_password',
    ));
}
add_action( 'rest_api_init', 'custom_forgot_password_route' );

// Custom function to handle forgot password
function custom_forgot_password( $data ) {
    $email = sanitize_email( $data['email'] );

    $user_data = get_user_by( 'email', $email );

    if ( ! $user_data ) {
        return new WP_Error( 'invalid_email', 'Email address not found.', array( 'status' => 404 ) );
    }

    $user_login = $user_data->user_login;
    $user_email = $user_data->user_email;

    // Generate new password reset key
    $key = get_password_reset_key( $user_data );

    // Construct reset password link
    $domain = $_SERVER['HTTP_HOST']; // Get the current domain
    $reset_link = "http://$domain/wp-json/custom/v1/reset-password/$key/";

    // Send reset password email
    $message = sprintf( __( 'Someone requested that the password be reset for the following account: %s' ), $user_email ) . "\r\n\r\n";
    $message .= __( 'If this was a mistake, just ignore this email and nothing will happen.' ) . "\r\n\r\n";
    $message .= $reset_link;

    $subject = __( 'Password Reset' );

    $sent = wp_mail( $user_email, $subject, $message );

    if ( ! $sent ) {
        return new WP_Error( 'email_error', 'Failed to send email.', array( 'status' => 500 ) );
    }

    return array( 'message' => 'Password reset email sent successfully.' );
}

//  ____                        _       ____                                                      _ 
// |  _ \    ___   ___    ___  | |_    |  _ \    __ _   ___   ___  __      __   ___    _ __    __| |
// | |_) |  / _ \ / __|  / _ \ | __|   | |_) |  / _` | / __| / __| \ \ /\ / /  / _ \  | '__|  / _` |
// |  _ <  |  __/ \__ \ |  __/ | |_    |  __/  | (_| | \__ \ \__ \  \ V  V /  | (_) | | |    | (_| |
// |_| \_\  \___| |___/  \___|  \__|   |_|      \__,_| |___/ |___/   \_/\_/    \___/  |_|     \__,_|
                                                                                                 

// Add custom endpoint for password reset
function custom_reset_password_route() {
    register_rest_route( 'custom/v1', '/reset-password/(?P<token>[\w-]+)', array(
        'methods' => 'POST',
        'callback' => 'custom_reset_password',
    ));
}
add_action( 'rest_api_init', 'custom_reset_password_route' );

// Custom function to handle password reset
function custom_reset_password( $data ) {
    $token = $data['token'];
    $new_password = $data['new_password'];

    // Validate token
    $user_id = reset_password( $token, $new_password );

    if ( is_wp_error( $user_id ) ) {
        return new WP_Error( 'invalid_token', $user_id->get_error_message(), array( 'status' => 400 ) );
    }

    return array( 'message' => 'Password reset successfully.' );
}


//  _              _       _                   _         
// (_) __      __ | |_    | |   ___     __ _  (_)  _ __  
// | | \ \ /\ / / | __|   | |  / _ \   / _` | | | | '_ \ 
// | |  \ V  V /  | |_    | | | (_) | | (_| | | | | | | |
// _/ |   \_/\_/    \__|   |_|  \___/   \__, | |_| |_| |_|
// |__/                                  |___/             

// Add custom endpoint for login
function custom_login_route() {
    register_rest_route( 'custom/v1', '/login', array(
        'methods' => 'POST',
        'callback' => 'custom_login',
    ));
}
add_action( 'rest_api_init', 'custom_login_route' );

// Custom function to handle login
function custom_login( $data ) {
    $username = $data['username'];
    $password = $data['password'];

    $user = wp_authenticate( $username, $password );

    if ( is_wp_error( $user ) ) {
        return new WP_Error( 'invalid_credentials', $user->get_error_message(), array( 'status' => 401 ) );
    }

    // Generate JWT token
    $token = jwt_auth_generate_token( $user->ID );

    if ( ! $token ) {
        return new WP_Error( 'jwt_error', 'Failed to generate JWT token.', array( 'status' => 500 ) );
    }

    // Get user email
    $user_email = $user->user_email;

    return array(
        'token' => $token,
        'email' => $user_email,
    );
}
