var myVar;

function myFunction() {
    document.getElementById("loader").style.display = "block";
    console.log('hlllo')
    myVar = setTimeout(showPage, 10000);
}

function showPage() {
    document.getElementById("loader").style.display = "none";
    console.log('done')
}

function formCreate(nameVal, typeVal, filetype, fileVal){
    var form = new FormData();
    form.append('name', nameVal);
    form.append('type', typeVal);
    form.append(filetype, fileVal);
    return form;
}

///////////////////////// upload image //////////////////////////////////////////////////////////////////////////////////
function uploadImage(){
    $.ajax({
    		type: 'POST',
            url: '/api/v1/upload/image',
            data: formCreate($('input[name="image"]').val(), 'local', 'image', $('input[name="pic_name"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
            	if(response.msg=='ok'){
                    console.log('Welcome Home im')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}

function uploadImage2(){
    $.ajax({
            type: 'POST',
            url: '/api/v2/upload/image',
            data: formCreate($('input[name="image"]').val(), 'gdrive', 'image', $('input[name="pic_name"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home im')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}

function uploadImage3(){
    $.ajax({
            type: 'POST',
            url: '/api/v3/upload/image',
            data: formCreate($('input[name="image"]').val(), 'cloudinary', 'image', $('input[name="pic_name"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home im')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}







////////////////////////// upload auio ////////////////////////////////////////////////////////////////////////////////

function uploadAudio(){
    $.ajax({
            type: 'POST',
            url: '/api/v1/upload/audio',
            data: formCreate($('input[name="song"]').val(), 'local', 'song', $('input[name="audio_name"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home au')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}

function uploadAudio2(){
    $.ajax({
            type: 'POST',
            url: '/api/v2/upload/audio',
            data: formCreate($('input[name="song"]').val(), 'gdrive', 'song', $('input[name="audio_name"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home au')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}

function uploadAudio3(){
    $.ajax({
            type: 'POST',
            url: '/api/v3/upload/audio',
            data: formCreate($('input[name="song"]').val(), 'cloudinary', 'song', $('input[name="audio_name"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home au')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}






///////////////////////// upload profile ///////////////////////////////////////////////////////////////////

function uploadProfile(){
    $.ajax({
            type: 'POST',
            url: '/api/v1/profilepic',
            data: formCreate("0", 'local', 'avatar', $('input[name="avatar"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home up')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}

function uploadProfile2(){
    $.ajax({
            type: 'POST',
            url: '/api/v2/profilepic',
            data: formCreate("0", 'gdrive', 'avatar', $('input[name="avatar"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home up')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}

function uploadProfile3(){
    $.ajax({
            type: 'POST',
            url: '/api/v3/profilepic',
            data: formCreate("0", 'cloudinary', 'avatar', $('input[name="avatar"]')[0].files[0]),
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home up')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                    alert(response.msg);
                }
            },
    });

}

///////////////////end/////////////////////////////////////////////////////////////////////////////////////////////



function login(){
    var username = $('#username').val();
    var password = $('#password').val();
    $.ajax({
        url: '/api/v1/login',
        data: {'username': username, 'password': password},
        type:"GET",
        dataType: 'json',
        crossDomain: true,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg);
                }
            },
            error: function(error) {
                console.log(error);
            },
    });
}

function register(){
    var username = $('#username').val();
    var password = $('#password').val();
    var email = $('#email').val();
    console.log(username);
    $.ajax({
        url: '/api/v1/signup',
        data: {'username': username, 'password': password, 'email': email},
        type:"POST",
        dataType: 'json',
        //crossDomain: true,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Registered')
                    window.location.assign(response.next_node);
                }
                else{
                    console.log(response.msg)
                }
                
            },
            error: function(error) {
                console.log(error);
            },
    });
}

function logout(){
    $.ajax({
        url: '/api/v1/logout',
        data: {'exit_code': '0'},
        type:"POST",
        dataType: 'json',
        crossDomain: true,
            success: function(response) {
                console.log(response.msg);
                window.location.assign(response.next_node);
            },
            error: function(error) {
                console.log(error);
            },
    });
}



function profiler(prof, name){
    return '<p id="showname">'+name+'</p>'+
        '<img src="'+prof+'"style="width: 150px; height:150px; border-radius: 50%;">';
}

function image_sign(prof, name){
    //'<p id="hjhjh">'+name+'</p>'+
    return '<img src="'+prof+'"style="width: 150px; height:150px; border-radius: 50%;">&nbsp;';
}

function audio_sign(prof, name){
    //'<div> <p>'+name+'</p>'+
    return '<audio controls>'+
            '<source src="'+prof+'" type="audio/mpeg">'+
            '</audio></div> &nbsp;';
}


function profiler2(prof, name){
    return '<p id="showname">'+name+'</p>'+
        '<img src="https://docs.google.com/uc?export=download&id='+prof+'"style="width: 150px; height:150px; border-radius: 50%;">';
}

function image_sign2(prof, name){
    //'<p id="hjhjh">'+name+'</p>'+
    return '<img src="https://docs.google.com/uc?export=download&id='+prof+'"style="width: 150px; height:150px; border-radius: 50%;">&nbsp;';
}

function audio_sign2(prof, name){
    //'<div> <p>'+name+'</p>'+
    return '<audio controls>'+
            '<source src="https://docs.google.com/uc?export=download&id='+prof+'" type="audio/mpeg">'+
            '</audio></div> &nbsp;';
}


function showContent(){
    document.getElementById("loader").style.display = "none";
    $.ajax({
        url: '/api/v1/user/data',
        data: {'type': '1'},
        type:"GET",
        dataType: 'json',
        crossDomain: true,
            success: function(response) {
                if(response.msg=='ok'){
                    $('#profile1_').append(profiler(response.profimg, response.username));

                    console.log(response.audioCount);
                    console.log(response.imageCount);
                    for (i = 0; i < response.audioCount; i++){
                        fn = response.audioN[i][1];
                        ln = response.audioN[i][0];
                        console.log(ln);
                        $('#audio1_').append(audio_sign(ln, fn));
                    }

                    for (i = 0; i < response.imageCount; i++){
                        fn = response.imageN[i][1];
                        ln = response.imageN[i][0];
                        console.log(ln)
                        $('#images1_').append(image_sign(ln, fn));
                    }


                }
            },
            error: function(error) {
                console.log(error);
            },
    });
}

function showContent2(){
    document.getElementById("loader").style.display = "none";
    $.ajax({
        url: '/api/v1/user/data',
        data: {'type': '2'},
        type:"GET",
        dataType: 'json',
        crossDomain: true,
            success: function(response) {
                if(response.msg=='ok'){
                    $('#profile1_').append(profiler2(response.profimg, response.username));

                    console.log(response.audioCount);
                    console.log(response.imageCount);
                    for (i = 0; i < response.audioCount; i++){
                        fn = response.audioN[i][1];
                        ln = response.audioN[i][0];
                        console.log(ln);
                        $('#audio1_').append(audio_sign2(ln, fn));
                    }

                    for (i = 0; i < response.imageCount; i++){
                        fn = response.imageN[i][1];
                        ln = response.imageN[i][0];
                        console.log(ln)
                        $('#images1_').append(image_sign2(ln, fn));
                    }


                }
            },
            error: function(error) {
                console.log(error);
            },
    });
}


function showContent3(){
    document.getElementById("loader").style.display = "none";
    $.ajax({
        url: '/api/v1/user/data',
        data: {'type': '3'},
        type:"GET",
        dataType: 'json',
        crossDomain: true,
            success: function(response) {
                if(response.msg=='ok'){
                    $('#profile1_').append(profiler(response.profimg, response.username));

                    console.log(response.audioCount);
                    console.log(response.imageCount);
                    for (i = 0; i < response.audioCount; i++){
                        fn = response.audioN[i][1];
                        ln = response.audioN[i][0];
                        console.log(ln);
                        $('#audio1_').append(audio_sign(ln, fn));
                    }

                    for (i = 0; i < response.imageCount; i++){
                        fn = response.imageN[i][1];
                        ln = response.imageN[i][0];
                        console.log(ln)
                        $('#images1_').append(image_sign(ln, fn));
                    }


                }
            },
            error: function(error) {
                console.log(error);
            },
    });
}

