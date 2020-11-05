class Index {
    static initPaginator() {
        document.body.querySelectorAll('.pagination > li > a')
                .forEach( link => link.addEventListener('click', Index.pagination_link_clickHandler) );
    }
    static pagination_link_clickHandler(event){
        event.preventDefault();
        let path = event.target.href;
        let page = Global.getURLParameter(path, 'page');
        if (typeof page !== 'undefined') {
            jQuery.ajax({
                url: jQuery(this).attr('action'),
                type: 'POST',
                data: {'page': getURLParameter(path, 'page')},
                success : function (json) {
                    if (json.result)
                    {
                        window.history.pushState({route: path}, "EVILEG", path);
                        jQuery("#post-list").replaceWith(articles);
                        Index.initPaginator();
                        jQuery(window).scrollTop(0);
                    }
                }
            });
        }
    }
}
Index.initPaginator();

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
