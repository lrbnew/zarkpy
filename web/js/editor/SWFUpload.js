var swfu;

$(function(){

    swfu = new SWFUpload({
        upload_url: "/post/userimage",
        flash_url  : "/plugins/swfupload/swfupload.swf",
        post_params: {
            "userid": 0
        },

        file_size_limit : "2 MB",
        file_types : "*.jpg;*.jpeg;*.gif;*.png;",
        file_types_description : "JPG/JPEG/GIF/PNG Images",
        file_upload_limit : "10",

        file_queue_error_handler : fileQueueError,
        file_dialog_complete_handler : fileDialogComplete,
        upload_progress_handler : uploadProgress,
        upload_error_handler : uploadError,
        upload_success_handler : uploadSuccess,
        upload_complete_handler : uploadComplete,

        button_image_url : "/plugins/swfupload/images/XPButtonText_100x22.png",
        button_placeholder_id : "swfupload_openselectfiles_btn",
        button_width: 100,
        button_height: 22,
        button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
        button_cursor: SWFUpload.CURSOR.HAND,

        custom_settings : { upload_target : "swfupload_progress_container" },
        debug: false
    });

});
