var more_success, more_fail;

if (DEBUG_DIR) {
    more_success = ['/site_media/css/theme.min.css'];
    more_fail = [
        '/site_media/js/public/min/core.min.js',
        '/site_media/css/core.min.css'
    ];
} else {
    more_success = [
        '/site_media/css/theme.css',
        '/site_media/css/palette.css'
    ];
    more_fail = [
        '/site_media/js/jquery.min.js',
        '/site_media/js/bootstrap.min.js',
        '/site_media/css/bootstrap.min.css'
    ].concat(more_success);
}

head.load('https://cdnjs.cloudflare.com/ajax/libs/jquery/' + js_ver.jquery + '/jquery.min.js', function() {
    head.test(window.jQuery, [
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + js_ver.bootstrap + '/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + js_ver.bootstrap + '/js/bootstrap.min.js'
    ].concat(more_success), more_fail, function() {
        $.ajaxSetup({'cache': true});
        if (window.location.pathname.indexOf('/group') != -1) {
            $.getScript('/site_media/js/group/' + DEBUG_DIR + 'menu' + DEBUG_STR + '.js');

        } else {
            $.getScript('/site_media/js/public/' + DEBUG_DIR + 'main' + DEBUG_STR + '.js');
        }
        $("head").append('<link rel="shortcut icon" href="/site_media/images/icon_daslab.png" />');
        $("head").append('<link rel="icon" type-"image/gif" href="/site_media/images/icon_daslab.png" />');
    });
});
