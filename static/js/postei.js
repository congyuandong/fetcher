//var html = '没有搜索到数据';
var runbar = 1;
var barpro = 0;
var progressbar = document.getElementById("progressbar");

//每次搜索的间隔时间
var search_time = 30;

function loadPage(){
	
	var times = $.cookie('times');
	if(times == null){
		$.cookie('times',0);
	}
	
	var load_timeout = $.cookie('load_timeout');
	if(load_timeout != 0 && load_timeout != null){
		$('#btn_search').attr('disabled', 'disabled');
		btn_disable();
	}
}

function dwr_postei() {
	
	
	
	var searchWord1 = document.getElementById("searchWord1").value.trim();
	if (searchWord1 == "" || searchWord1 == null) {
		$('#searchWord1').popover('show');
		return;
	} else {
		// 按钮不可用
		$('#btn_search').attr('disabled', 'disabled');
		$.cookie('load_timeout',search_time);
		btn_disable();
		// $('#btn_search').text("123");
	}

	var no_progressbar = document.getElementById("no_progressbar");
	var detail_panel = document.getElementById("detail_panel");
	var detail_load = document.getElementById("detail_load");

	// window.open("detail.jsp?searchWord1=" + searchWord1);
	detail_panel.style.display = 'block';
	detail_load.style.display = 'none';
	progressbar.style.display = 'block';
	// no_progressbar.style.display = 'none';
	runbar = 1;
	barpro = 0;
	run();
	$.get("/f/web/", {
			'title': searchWord1
		},
		function(data, status) {
			if(data.status == 1){
				detail_load.style.display = 'block';
				progressbar.style.display = 'none';
						// $('#btn_search').attr('disabled', false);
						// $('#btn_search').text("Search");
				unbar = 0;
				document.getElementById("detail_load").innerHTML = data.body;
				checkSearchTimes();
			}else {
				detail_load.style.display = 'block';
				progressbar.style.display = 'none';
				// $('#btn_search').attr('disabled', false);
				// $('#btn_search').text("Search");
				runbar = 0;
				document.getElementById("detail_load").innerHTML = '未检索到数据，可能由于网络请求超时造成，请重试';
			}
		});

}

function btn_disable() {
	var load_timeout = $.cookie('load_timeout');
	if (load_timeout >= 0) {
		$('#btn_search').text(load_timeout+'s');
		$.cookie('load_timeout' , load_timeout - 1);
		var timer = setTimeout("btn_disable()", 1000);
	}else{
		$('#btn_search').attr('disabled', false);
		$('#btn_search').text('Search');
	}
	
}


function checkSearchTimes(){
	var times = parseInt($.cookie('times'));
	times += 1;
	$.cookie('times' , times);
	//alert(times);
	if(times == 3){
		$('#modal_donate').modal('show');
	}
}

function run() {
	if (runbar != 1)
		return;
	// 在最后的20%逐渐减速，好吧，只是骗骗观众的~~
	if (barpro < 80)
		barpro += 1;
	else
		barpro += (100 - barpro) / 20;
	$("div[class=progress-bar]").css("width", barpro + "%");
	if (barpro < 100) {
		var timer = setTimeout("run()", 100);
	} else {
		barpro = 0;
		// $("div[class=progress-bar]").progressbar('setPosition', 0);
		// var timer=setTimeout("run()",100);
		return;
	}
}

function loadtable() {
	// alert(1);
	// $(document).ready(function() {
	// document.getElementById("detail_load").innerHTML = html;
	// });
	var url = location.search;
	// var progressbar = document.getElementById("progressbar");

	if (url.indexOf("?") != -1) {
		var str = url.substr(1);
		strs = str.split("=");
		// alert(strs[1]);
		SearchEI
				.SearchBySearchWord1(
						strs[1],
						function callback(data) {
							if (data) {
								// progressbar.style.display='none';
								document.getElementById("detail_load").innerHTML = data;
							} else {
								// progressbar.style.display='none';
								document.getElementById("detail_load").innerHTML = '未检索到数据，可能由于网络请求超时造成，请重试';
							}
						});
	}
}

function donate() {
	window.open('http://me.alipay.com/congyuandong');
	// window.location = 'http://me.alipay.com/congyuandong';
}
