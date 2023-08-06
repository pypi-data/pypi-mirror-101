 	function toDecimal(x) {
            var f = parseFloat(x);  
            if (isNaN(f)) {  
                return;  
            }  
            f = Math.round(x*100)/100;  
            return f;  
    }  
	function to_byte(value, dec) {
    	if (value == 0) 
        	return '0';
        var prefix_list = ['B', 'K', 'M', 'G', 'T'];
		var t = 1;
		
		//for(;dec>0;t*=10,dec--);
		
		//for(;dec<0;t/=10,dec++); 
			        
        //value =  Math.round(value*t)/t;
        value =  Math.round(value); 
        var i = 0;
        while (value >= 1000){
			value /= 1000;
            i = i+1;       	
        }
        // while (value >= 1024){
			// value /= 1024
            // i = i+1	        	
        // }
        //return Math.round(value*t)/t + prefix_list[i]
        return Math.round(value) + prefix_list[i];
    }
    
	        
	$(function() {
		var fileTemplate = "<div id=\"{id}\">";
		fileTemplate += "<div class=\"progress progress-striped active\"><div class=\"progress-bar bar\" style=\"width: 0%\"></div></div>";
		fileTemplate += "</div>";
		function slugify(text) {
			text = encodeURIComponent(text);
			text = text.replace(/[^-a-zA-Z0-9,&\s]+/ig, '');
			text = text.replace(/-/gi, "_");
			text = text.replace(/\s/gi, "-");
			return text;
		}

		var target_id = $("#target_id").val();
		$(".dropbox, .zipUpload").html5Uploader({
			postUrl : "/upload/?format=json&&file_type=zip",
			file_ext:["zip", "rar",'jpg','png'],
			upload_limit:1,
			max_size:1000000000,
			onClientLoadStart : function(e, file) {
				alert(slugify(file.name))
				$('.sign-tip').hide();
				if (file.name.toLowerCase().indexOf('.apk') != -1) {
				}
				var upload = $(".file_list");
				if (upload.is(":hidden")) {
					upload.show();
				}
				upload.html(fileTemplate.replace(/{id}/g, slugify(file.name)));
			},
			onClientLoad : function(e, file) {
				
			},
			onServerLoadStart : function(e, file) {
				$("#" + slugify(file.name)).find(".bar").css('width', '0%').html('0%');
			},
			onServerProgress : function(e, file) {
				if (e.lengthComputable) {
					var percentComplete = (e.loaded / e.total) * 100;
					$("#" + slugify(file.name)).find(".bar").css('width', percentComplete + '%').html(toDecimal(percentComplete) + '%');
				}
			},
			onServerLoad : function(e, file) {

				$("#" + slugify(file.name)).find(".bar").css('width', '100%').html('100%');
			},
			onSuccess : function(e, file, data) {
            console.dir(this)
            console.dir(e)
            console.dir(file)
				eval("var data =" + data);
				if (data.code == "0") {
					$("#zip_cont").attr("value",data.file_url);
				}
				else {
					alert(data);

				}
			}			
			
		});
	});

