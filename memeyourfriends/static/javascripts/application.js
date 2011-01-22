/* Application Javascript */
function _Application() {
    var APP_ID = "1c6f5e338c7989f098ad50f8c1224878";
    var MEME_GEN = "http://www.willhughes.ca:8080";

    function loadFBAPIComplete(response) {
	if (response.session) {
	    $("#create_step").show();
	} else {
	    $("#login_step").show();
	}
    }

    function selectPhoto() {
	FB.api('/me/albums', loadAlbumsComplete);
    }

    function loadAlbumsComplete(response) {
	$.each(response.data, function() {
		FB.api('/' + this.id + '/photos', loadAlbumPhotosComplete);
	    });
    }

    function loadAlbumPhotosComplete(response) {
	$.each(response.data, function() {
		var img, div, data;
		data = this;
		img = $("<img />");
		img.attr("src", data.picture);
		img.addClass("selectImg");
		//		img.cjObjectScaler({method:"fill"});
		img.click(function() {
			photoSelected(data.source);
		    });
		div = $("<div />");
		div.append(img);
		div.addClass("selectDiv");
		$("#photos").append(div);
	    });
    }

    function photoSelected(source) {
	var img;
	$("input[name='imgSrc']").val(source);
	img = $("<img />");
	img.attr("src", source);
	img.cjObjectScaler({method:"fill"});
	$("#photo_display").html(img);
	$("#photo_prompt").hide();
    }

    function submit() {
	var top, bot, url;
	url = $("input[name='imgSrc']").val();
	top = $("input[name='caption1']").val();
	bot = $("input[name='caption2']").val();
	$("#meme_frame").attr("src", MEME_GEN + '?url=' + url + '&top=' + top + '&bot=' + bot);
	//	$.post(MEME_GEN, {top:top, bot:bot, url:url},
	//	       submitComplete);
    }

    function submitComplete(response) {
	alert(response);
    }

    function initApplication() {
	FB.init({appId: APP_ID,
		    status: true,
		    cookie: true,
		    xfbml: true});
	FB.getLoginStatus(loadFBAPIComplete);
	selectPhoto();
	//	$("#photo_container").click(selectPhoto);
	$("#submit").click(submit);
    }
    $(initApplication);

}

var Application = new _Application();