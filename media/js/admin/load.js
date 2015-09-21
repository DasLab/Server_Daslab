var xmlhttp = new XMLHttpRequest(), isCDN = false;
var ver_jquery, ver_bootstrap, ver_swfobj, ver_fullcal, ver_moment, ver_dropz;
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == XMLHttpRequest.DONE) {
    	if (xmlhttp.status == 200) {
			var xmlDoc = xmlhttp.responseText.split(/\t/);
			ver_jquery = xmlDoc[11];
			ver_bootstrap = xmlDoc[12];
			ver_swfobj = xmlDoc[16];
			ver_fullcal= xmlDoc[17];
			ver_moment = xmlDoc[18];
			// ver_dropz = xmlDoc[19];

			document.write('<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/' + ver_jquery + '/jquery.min.js"><\/script>');
			document.write('<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + ver_bootstrap + '/js/bootstrap.min.js"><\/script>');
			document.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + ver_bootstrap + '/css/bootstrap.min.css" \/>');
			document.write('\
				<script type="text/javascript"> \
					if (!window.jQuery) { \
						document.write(\'<script type="text/javascript" src="/site_media/js/jquery.min.js"><\' + \'/script>\'); \
						document.write(\'<script type="text/javascript" src="/site_media/js/bootstrap.min.js"><\' + \'/script>\'); \
						document.write(\'<link rel="stylesheet" href="/site_media/css/bootstrap.min.css" \/>\'); \
						isCDN = false; \
					} else { \
						isCDN = true; \
					} \
				\x3C\/script>');
		} else {
			document.write('<script type="text/javascript" src="/site_media/js/jquery.min.js"><\/script>');
			document.write('<script type="text/javascript" src="/site_media/js/bootstrap.min.js"><\/script>');
			document.write('<link rel="stylesheet" href="/site_media/css/bootstrap.min.css" \/>');
		}
		document.write('<link rel="stylesheet" href="/site_media/css/theme.css" \/>');
		document.write('<link rel="stylesheet" href="/site_media/css/palette.css" \>');
		document.write('<link rel="shortcut icon" href="/site_media/images/icon_daslab.png" \/>');
		document.write('<link rel="icon" type-"image/gif" href="/site_media/images/icon_daslab.png" \/>');
	}
}
xmlhttp.open("GET", "/site_data/stat_sys.txt", false);
xmlhttp.send();
