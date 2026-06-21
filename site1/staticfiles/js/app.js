$(document).ready(function() {
    var istextsteg = true;
    var coverimage;
    /* Encode Section */

    $("#encodeForm").submit(function(event) {
        event.preventDefault();
        $('.err-res').html('');
        $('#submitbtn').hide();
        coverimage = $("#encodeimg").prop("files")[0];
        var coverText = $("#message").val();

        if(coverimage && isImageValid(coverimage.name) && isvalidSize(coverimage.size)) {
            $('#loader').show();
            var formData =  new FormData();
            var to = $("#to").val();
            if(to!=0){
                formData.append('to',to)
            }
            formData.append('coverimage', $("#encodeimg").prop("files")[0]);
            formData.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
            if(istextsteg) {
                formData.append('istextsteg', true);
                formData.append('message', coverText);
                if(formData.has('textfile')){formData.delete('textfile');};
                // for(var pair of formData.entries()){
                //         console.log(pair[0], pair[1]);
                // }
                
            } else {
                if(formData.has('istextsteg')){formData.delete('istextsteg');};
                formData.append('textfile', $("#encodetextfile").prop("files")[0]);
                if(formData.has('message')){formData.delete('message');};
            }
            $.ajax({
                url: '/myapp/process_encoding_data',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data);
                    $("#encodeForm").trigger("reset");
                    $('#submitbtn').show();
                    $('#Upfilename').html('');
                    $('#UpTextfilename').html('');
                    $('#loader').hide();
                    var a = $("<a>")
                        .attr("href", data.location)
                        .attr("target", "_blank")
                        .attr("download", data.location.replace(/^.*\./, ''))
                        .appendTo("body");
                        a[0].click();
                        a.remove();
                },
                error: function (jqXHR, exception) {
                    $('#submitbtn').hide();
                    $('#Upfilename').html('');
                    $('#UpTextfilename').html('');
                    $('#loader').hide();
                }
             });

        } else {
            $("#encodeForm").trigger("reset");
            $('#submitbtn').show();
            $('#Upfilename').html('');
            $('.err-res').html('Error Occured');
        }
    });

    $("#encodeimg").change(function() {
        $('#Upfilename').html($(this).val().split('\\').pop());
        $('#message').focus();
        $('.err-res').html('');
    });

    $('#encodetextfile').change(function() {
        var textfile = $("#encodetextfile").prop("files")[0];
        if(isTextFileValid(textfile.name)) {
            $('#UpTextfilename').html($(this).val().split('\\').pop());
            $('.err-res-txt').html('');
        } else {
            $("#encodetextfile").val(null);
            $('#UpTextfilename').html('');
            $('.err-res-txt').html('Error with text file');
        }
        
    });

    /* tab section */

    $('.tab-section').click(function(){
        $('.tab-section').removeClass('tab-active');
        $('.tab-content').removeClass('show-tab');
        $(this).addClass('tab-active');
        var tabcontentid = $(this).attr('tab-id');
        $('#' + tabcontentid).addClass('show-tab');
        if(tabcontentid == 'encText' || tabcontentid == 'decText') {
            istextsteg = true;
            $("#encodetextfile").prop('required',false);
        } else {
            $("#encodetextfile").prop('required',true);
            istextsteg = false; 
        }
    })

    /* Decode Section */

    $("#decodeForm").submit(function(e) {
        e.preventDefault();
        $('.err-res').html('');
        $('#desubmitbtn').hide();
        $('.decode-text').hide();
        var stegImage = $("#decodeimg").prop("files")[0];
        if(isImagepng(stegImage.name)) {
            $('#loader').show();
            var formData =  new FormData();
            formData.append('stegimage', stegImage);
            formData.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
            if(istextsteg) {
                formData.append('istextsteg', true);
            }
            $.ajax({
                url: '/myapp/process_decoding_data',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data);
                    if(data.message) {
                        $('.decode-text').show();
                        $('.decode-text').find('span').text(data.message);
                    }
                    if(data.location) {
                        var a = $("<a>")
                        .attr("href", data.location)
                        .attr("target", "_blank")
                        .attr("download", data.location.replace(/^.*\./, ''))
                        .appendTo("body");
                        a[0].click();
                        a.remove();
                    }
                    $("#decodeForm").trigger("reset");
                    $('#desubmitbtn').show();
                    $('#Upfilename').html('');
                    $('#loader').hide();
                },
                error: function (jqXHR, exception) {
                    console.log('error');
                    $('#desubmitbtn').hide();
                    $('#Upfilename').html('');
                    $('#loader').hide();
                }
            });
        } else {
            $("#decodeForm").trigger("reset");
            $('#desubmitbtn').show();
            $('#Upfilename').html('');
            $('.err-res').html('Error with File');
        }
    });

    
    $("#decodeimg").change(function() {
        $('#Upfilename').html($(this).val().split('\\').pop());
        $('.err-res').html('');
    });

});



function isImageValid(fileName) {
    var extension = fileName.replace(/^.*\./, '');
    if (extension == fileName) { return false; }
    extension = extension.toLowerCase();
    if(extension ==='jpg' || extension ==='png' || extension ==='jpeg') {
        return true
    } else {
        return false;
    }
}

function isTextFileValid(fileName) {
    var extension = fileName.replace(/^.*\./, '');
    if (extension == fileName) { return false; }
    extension = extension.toLowerCase();
    if(extension ==='txt') {
        return true
    } else {
        return false;
    }
}

function isImagepng(fileName) {
    var extension = fileName.replace(/^.*\./, '');
    if (extension == fileName) { return false; }
    extension = extension.toLowerCase();
    if(extension ==='png') {
        return true
    } else {
        return false;
    }
}

function isvalidSize(totalBytes) {
    var _size = Math.floor(totalBytes/1000);
    if(_size <= 800) {
        return true
    }else {
        return false;
    }
}

const decode_image_url = async (image)=>{
    const res =  await fetch(`/myapp/decode_image_url?image=${image}`)
    const data  = await res.json()
    // alert(data.message)
    document.getElementById('#messageBody').innerHTML = data.message;
    $('#messageModal').modal('toggle');
}