var more_success, more_fail;

if (app.DEBUG_DIR) {
    more_success = [
        '/site_media/js/suit/min/core.min.js',
        '/site_media/css/_suit.css',
        '/site_media/css/min/theme.min.css'
    ];
    more_fail = [
        '/site_media/js/public/min/core.min.js',
        '/site_media/js/suit/min/core.min.js',
        '/site_media/css/suit.min.css',
        '/site_media/css/min/core.min.css'
    ];
} else {
    more_success = [
        '/site_media/js/suit/core.js',
        '/site_media/css/_suit.css',
        '/site_media/css/theme.css',
        '/site_media/css/palette.css'
    ];
    more_fail = [
        '/site_media/js/jquery.min.js',
        '/site_media/js/bootstrap.min.js',
        '/site_media/css/bootstrap.min.css'
    ].concat(more_success);
}

head.load('https://cdnjs.cloudflare.com/ajax/libs/jquery/' + app.js_ver.jquery + '/jquery.min.js', function() {
    head.test(window.$, [
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/js/bootstrap.min.js'
    ].concat(more_success), more_fail, function(flag) {
        app.isCDN = flag;
        $.ajaxSetup({'cache': true});
        if (!app.DEBUG_DIR) {
            $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + '_suit' + app.DEBUG_STR + '.js');
            $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'table' + app.DEBUG_STR + '.js');
            $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'clock' + app.DEBUG_STR + '.js');
        }
        $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'menu' + app.DEBUG_STR + '.js');

        google.charts.load('visualization', '1', {packages: ['corechart', 'calendar', 'map']});

        $("head").append('<link rel="shortcut icon" href="/site_media/images/icon_daslab.png" />');
        $("head").append('<link rel="icon" type-"image/gif" href="/site_media/images/icon_daslab.png" />');
    });
});
