function show_hide_password(target){
	var input = document.getElementById('password-input');
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
}

function to_bookmarks(){
    var current = $(this);
    var type = current.data('type');
    var pk = current.data('id');
    var action = current.data('action');
    $.ajax({
        url : '/api/' + type + '/' + pk + '/' + action + '/',
        type : 'POST',
        data : { 'obj' : pk },
        success : function (json) {
            current.find("[data-count='" + action + "']").text(json.count);
        }
    });
    return false;
}
