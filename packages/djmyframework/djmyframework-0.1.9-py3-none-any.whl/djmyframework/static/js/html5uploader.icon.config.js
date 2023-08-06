	$(function() {
		var fileTemplate = "<div id=\"{id}\">";
		fileTemplate += "<div class=\"icon\"></div>";
		fileTemplate += "<div class=\"progress progress-striped active\"><div class=\"bar\" style=\"width: 0%\"></div></div>";
		fileTemplate += "</div>";
		function slugify(text) {
			text = encodeURIComponent(text);
			text = text.replace(/[^-a-zA-Z0-9,&\s]+/ig, '');
			text = text.replace(/-/gi, "_");
			text = text.replace(/\s/gi, "-");
			return text;
		}
		var file_type = $("#file_type").val() || '';
		$(".dropbox, .imageUpload").html5Uploader({
			postUrl : "/upload/?target_id="+$("#target_id").val()+"&file_type=" + file_type + "&format=json",
			file_ext:["jpg","jpeg","png"],
			upload_limit:1,
			max_size:200000,//200k
			onClientLoadStart : function(e, file) {
				var upload = $(".file_list");
				if (upload.is(":hidden")) {
					upload.show();
				}
				upload.html(fileTemplate.replace(/{id}/g, slugify(file.name)));
			},
			onClientLoad : function(e, file) {
				$("#" + slugify(file.name)).find(".icon	").attr("style", "background-image:url('" + e.target.result + "')");
			},
			onServerLoadStart : function(e, file) {
				$("#" + slugify(file.name)).find(".bar").css('width', '0%');
			},
			onServerProgress : function(e, file) {
				if (e.lengthComputable) {
					var percentComplete = (e.loaded / e.total) * 100;
					$("#" + slugify(file.name)).find(".bar").css('width', percentComplete + '%');

				}
			},
			onServerLoad : function(e, file) {
				$("#" + slugify(file.name)).find(".bar").css('width', '100%');
				$("#" + slugify(file.name)).find(".progress-bar").fadeOut();
			},
			onSuccess : function(e, file, data) {
				var data = JSON.parse(data)
				if (data.code == "0") {
					$("#file_url").attr("value",data.file_url);
					$("#icon").attr("value",data.file_url);
					$(".icon").css("background-image",'url('+$("#icon").val()+')');
				}
				else {
					$("#" + slugify(file.name)).find(".icon	").html('上传失败!')		
				}
				$("#" + slugify(file.name)).find(".progress").hide();
			}			
		});
	});