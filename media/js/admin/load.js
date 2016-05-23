head.load('https://cdnjs.cloudflare.com/ajax/libs/jquery/' + js_ver.jquery + '/jquery.min.js', function() {
    head.test(window.jQuery, [
            'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + js_ver.bootstrap + '/css/bootstrap.min.css',
            'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + js_ver.bootstrap + '/js/bootstrap.min.js'
        ], [
            '/site_media/js/jquery.min.js',
            '/site_media/css/bootstrap.min.css',
            '/site_media/js/bootstrap.min.js'
        ], function() {
            $.ajaxSetup({'cache': true});
            $.getScript('/site_media/js/public/' + DEBUG_DIR + 'main' + DEBUG_STR + '.js');
            $("head").append('<link rel="shortcut icon" href="/site_media/images/icon_daslab.png" />');
            $("head").append('<link rel="icon" type-"image/gif" href="/site_media/images/icon_daslab.png" />');
        });
});



//         if (DEBUG_DIR) {
//             document.write('<link rel="stylesheet" href="/site_media/css/' + DEBUG_DIR + 'theme' + DEBUG_STR + '.css" \/>');
//         } else {
//             document.write('<link rel="stylesheet" href="/site_media/css/theme.css" \/>');
//             document.write('<link rel="stylesheet" href="/site_media/css/palette.css" \/>');

