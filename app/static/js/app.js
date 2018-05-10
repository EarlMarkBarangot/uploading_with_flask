function uploadImage(){
	var form = new FormData();
    form.append('name', $('input[name="image"]').val());
    form.append('image', $('input[name="pic_name"]')[0].files[0]);

    $.ajax({
    		type: 'POST',
            url: '/api/upload/image',
            data: form,
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
                    console.log(response.msg)
                }
            },
    });

}

function uploadAudio(){
    var form = new FormData();
    form.append('name', $('input[name="song"]').val());
    form.append('song', $('input[name="audio_name"]')[0].files[0]);

    $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/upload/audio',
            data: form,
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home au')
                    window.location.assign(response.next_node);
                }
            },
    });

}

function uploadProfile(){
    var form = new FormData();
    form.append('avatar', $('input[name="avatar"]')[0].files[0]);

    $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/profilepic',
            data: form,
            cache: false,
            contentType: false,
            processData: false,
            async: false,
            success: function(response) {
                if(response.msg=='ok'){
                    console.log('Welcome Home up')
                    window.location.assign(response.next_node);
                }
            },
    });

}



function login(){
    var username = $('#username').val();
    var password = $('#password').val();
    $.ajax({
        url: 'http://127.0.0.1:5000/api/login',
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
        url: 'http://127.0.0.1:5000/api/signup',
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
        url: 'http://127.0.0.1:5000/api/logout',
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
    return '<p id="hjhjh">'+name+'</p>'+
        '<img src="'+prof+'"style="width: 150px; height:150px; border-radius: 50%;">';
}

function audio_sign(prof, name){
    return '<div> <p>'+name+'</p>'+
    '<audio controls>'+
            '<source src="'+prof+'" type="audio/mpeg">'+
            '</audio></div>';
}

function showContent(){
    $.ajax({
        url: 'http://127.0.0.1:5000/api/user/data',
        data: {'exit_code': '0'},
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

