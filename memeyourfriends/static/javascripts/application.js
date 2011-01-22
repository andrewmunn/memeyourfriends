/* Application Javascript */
function _Application() {
    var APP_ID = "1c6f5e338c7989f098ad50f8c1224878";

    function loadFBAPI() {
	var e = document.createElement('script');
	e.async = true;
	e.src = document.location.protocol +
	    '//connect.facebook.net/en_US/all.js';
	$('#fb-root').append($(e));
    }

    function loadFBAPIComplete(response) {
	if (response.session) {
	    $("#create_step").show();
	} else {
	    $("#login_step").show();
	}
    }

    function friendSelected() {
	var fbid = $("#fb_friends").val();
	FB.api('/' + fbid + '/photos', loadFriendPhotosComplete);
    }

    function loadFriendPhotosComplete(response) {
	$.each(response.data, function() {
		var img = $("<img />");
		img.attr("src", this.picture);
		$("#photos_step .content").append(img);
	    });
    }

    function initApplication() {
	loadFBAPI();
    }
    $(initApplication);

    window.fbAsyncInit = function() {
	FB.init({appId: APP_ID,
		 status: true,
		 cookie: true,
		 xfbml: true});
	FB.getLoginStatus(loadFBAPIComplete);
    };    
}

var Application = new _Application();