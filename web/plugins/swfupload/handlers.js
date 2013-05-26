var initSWFUpload = (function(){

    var OPENER_ID = 'swfupload_openselectfiles_btn', // 选择上传图片的按钮id
        PROGRESS_CONTAINER_ID = 'swfupload_progress_container', // 上传进度条id
        THUMBNAILS_ID = 'exists_user_image', // 已上传图片div id
        ERROR_IMAGE = '/plugins/swfupload/images/error.gif',
        DEBUG = false;

    // ../cgi/api/UserImage.py
    function addImage(src, img_id, img_name) {
        var img_html;
        if (img_id){
            img_html = '<div class="col3_padding" js="one_user_image" id="choose_image_' + img_id + '" onchange="modifyUserImage(' + img_id + ');"><img src="' + src + '" ondblclick="chooseUserImage(this,' + img_id + ');return false;" /><input type="text" js="file_name" value="' + img_name + '" /><br/><p>ID: '+img_id+'</p><a class="link_del trans" href="javascript:void(0);" onclick="deleteUserImage(this, ' + img_id + '); return false;">删除</a></div>';
        }else{
            img_html = '<div><img src="'+src+'" /></div>';
        };

        $(img_html).hide().prependTo('#' + THUMBNAILS_ID).fadeIn();
    }

    function fileQueueError(file, errorCode, message) {
        try {
            var imageName = ERROR_IMAGE;
            var errorName = "";
            if (errorCode === SWFUpload.errorCode_QUEUE_LIMIT_EXCEEDED) {
                errorName = "您选择的文件太多了.";
            }

            if (errorName !== "") {
                return;
            }

            switch (errorCode) {
                case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
                    imageName = "/plugins/swfupload/images/zerobyte.gif";
                    break;
                case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
                    imageName = "/plugins/swfupload/images/toobig.gif";
                    break;
                case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
                case SWFUpload.QUEUE_ERROR.INVALID_FILETYPE:
                default:
                    break;
            }

            addImage(imageName);

        } catch (ex) {
            this.debug(ex);
        }

    }

    function fileDialogComplete(numFilesSelected, numFilesQueued) {
        try {
            if (numFilesQueued > 0) {
                this.startUpload();
            }
        } catch (ex) {
            this.debug(ex);
        }
    }

    function uploadProgress(file, bytesLoaded) {
        try {
            var percent = Math.ceil((bytesLoaded / file.size) * 100);

            var progress = new FileProgress(file,  this.customSettings.upload_target);
            progress.setProgress(percent);
            if (percent === 100) {
                progress.setStatus("创建缩略图...");
                progress.toggleCancel(false, this);
            } else {
                progress.setStatus("上传中...");
                progress.toggleCancel(true, this);
            }
        } catch (ex) {
            this.debug(ex);
        }
    }

    function uploadSuccess(file, serverData) {
        try {
            var progress = new FileProgress(file,  this.customSettings.upload_target);

            if (serverData.substring(0, 8) === "success;") {
                var user_image_id = serverData.substring(8).split(';')[0]
                var image_src = serverData.substring(8).split(';')[1]
                var image_name = serverData.substring(8).split(';')[2]
                addImage(image_src, user_image_id, image_name);
                progress.setStatus(""); //Thumbnail Created.
                progress.toggleCancel(false);
            } else {
                addImage(ERROR_IMAGE);
                progress.setStatus("Error.");
                progress.toggleCancel(false);
            }

        } catch (ex) {
            this.debug(ex);
        }
    }

    function uploadComplete(file) {
        try {
            /*  I want the next upload to continue automatically so I'll call startUpload here */
            if (this.getStats().files_queued > 0) {
                this.startUpload();
            } else {
                var progress = new FileProgress(file,  this.customSettings.upload_target);
                progress.setComplete();
                progress.setStatus("上传完毕");
                progress.toggleCancel(false);
            }
        } catch (ex) {
            this.debug(ex);
        }
    }

    function uploadError(file, errorCode, message) {
        var imageName =  ERROR_IMAGE,
            progress;

        try {
            switch (errorCode) {
                case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
                    try {
                        progress = new FileProgress(file,  this.customSettings.upload_target);
                        progress.setCancelled();
                        progress.setStatus("已取消");
                        progress.toggleCancel(false);
                    }
                    catch (ex1) {
                        this.debug(ex1);
                    }
                    break;
                case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
                    try {
                        progress = new FileProgress(file,  this.customSettings.upload_target);
                        progress.setCancelled();
                        progress.setStatus("已停止");
                        progress.toggleCancel(true);
                    }
                    catch (ex2) {
                        this.debug(ex2);
                    }
                case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:
                    imageName = "/plugins/swfupload/images/uploadlimit.gif";
                    break;
                default:
                    break;
            }

            addImage(imageName);

        } catch (ex3) {
            this.debug(ex3);
        }

    }

    function fadeIn(element, opacity) {
        var reduceOpacityBy = 5;
        var rate = 30;	// 15 fps

        if (opacity < 100) {
            opacity += reduceOpacityBy;
            if (opacity > 100) {
                opacity = 100;
            }

            if (element.filters) {
                try {
                    element.filters.item("DXImageTransform.Microsoft.Alpha").opacity = opacity;
                } catch (e) {
                    // If it is not set initially, the browser will throw an error.  This will set it if it is not set yet.
                    element.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=' + opacity + ')';
                }
            } else {
                element.style.opacity = opacity / 100;
            }
        }

        if (opacity < 100) {
            setTimeout(function () {
                fadeIn(element, opacity);
            }, rate);
        }
    }



    /* ******************************************
     *	FileProgress Object
     *	Control object for displaying file info
     * ****************************************** */

    function FileProgress(file, targetID) {
        this.fileProgressID = "divFileProgress";

        this.fileProgressWrapper = document.getElementById(this.fileProgressID);
        if (!this.fileProgressWrapper) {
            this.fileProgressWrapper = document.createElement("div");
            this.fileProgressWrapper.className = "progressWrapper";
            this.fileProgressWrapper.id = this.fileProgressID;

            this.fileProgressElement = document.createElement("div");
            this.fileProgressElement.className = "progressContainer";

            var progressCancel = document.createElement("a");
            progressCancel.className = "progressCancel";
            progressCancel.href = "#";
            progressCancel.style.visibility = "hidden";
            progressCancel.appendChild(document.createTextNode(" "));

            var progressText = document.createElement("div");
            progressText.className = "progressName";
            progressText.appendChild(document.createTextNode(file.name));

            var progressBar = document.createElement("div");
            progressBar.className = "progressBarInProgress";

            var progressStatus = document.createElement("div");
            progressStatus.className = "progressBarStatus";
            progressStatus.innerHTML = "&nbsp;";

            this.fileProgressElement.appendChild(progressCancel);
            this.fileProgressElement.appendChild(progressText);
            this.fileProgressElement.appendChild(progressStatus);
            this.fileProgressElement.appendChild(progressBar);

            this.fileProgressWrapper.appendChild(this.fileProgressElement);

            document.getElementById(targetID).appendChild(this.fileProgressWrapper);
            fadeIn(this.fileProgressWrapper, 0);

        } else {
            this.fileProgressElement = this.fileProgressWrapper.firstChild;
            this.fileProgressElement.childNodes[1].firstChild.nodeValue = file.name;
        }

        this.height = this.fileProgressWrapper.offsetHeight;

    }
    FileProgress.prototype.setProgress = function (percentage) {
        this.fileProgressElement.className = "progressContainer green";
        this.fileProgressElement.childNodes[3].className = "progressBarInProgress";
        this.fileProgressElement.childNodes[3].style.width = percentage + "%";
    };
    FileProgress.prototype.setComplete = function () {
        this.fileProgressElement.className = "progressContainer blue";
        this.fileProgressElement.childNodes[3].className = "progressBarComplete";
        this.fileProgressElement.childNodes[3].style.width = "";

    };
    FileProgress.prototype.setError = function () {
        this.fileProgressElement.className = "progressContainer red";
        this.fileProgressElement.childNodes[3].className = "progressBarError";
        this.fileProgressElement.childNodes[3].style.width = "";

    };
    FileProgress.prototype.setCancelled = function () {
        this.fileProgressElement.className = "progressContainer";
        this.fileProgressElement.childNodes[3].className = "progressBarError";
        this.fileProgressElement.childNodes[3].style.width = "";

    };
    FileProgress.prototype.setStatus = function (status) {
        this.fileProgressElement.childNodes[2].innerHTML = status;
    };

    FileProgress.prototype.toggleCancel = function (show, swfuploadInstance) {
        this.fileProgressElement.childNodes[0].style.visibility = show ? "visible" : "hidden";
        if (swfuploadInstance) {
            var fileID = this.fileProgressID;
            this.fileProgressElement.childNodes[0].onclick = function () {
                swfuploadInstance.cancelUpload(fileID);
                return false;
            };
        }
    };

    return function(user_id){
        return new SWFUpload({
            upload_url : "/api/user-image",
            flash_url  : "/plugins/swfupload/swfupload.swf",
            post_params: {
                "action": 'postImage',
                "Userid": user_id
            },

            file_size_limit : "2 MB",
            file_types : "*.jpg;*.jpeg;*.gif;*.png;",
            file_types_description : "JPG/JPEG/GIF/PNG Images",
            file_upload_limit : "100",

            file_queue_error_handler : fileQueueError,
            file_dialog_complete_handler : fileDialogComplete,
            upload_progress_handler : uploadProgress,
            upload_error_handler : uploadError,
            upload_success_handler : uploadSuccess,
            upload_complete_handler : uploadComplete,

            button_image_url : "/plugins/swfupload/images/XPButtonText_105x30.png",
            button_placeholder_id : OPENER_ID,
            button_width: 105,
            button_height: 30,
            button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
            button_cursor: SWFUpload.CURSOR.HAND,

            custom_settings : { upload_target : PROGRESS_CONTAINER_ID },
            debug: DEBUG
        });

    };

})();
