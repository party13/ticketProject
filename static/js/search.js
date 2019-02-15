
console.log('loaded search Functionality');

var st = document.querySelector('#search_input');
console.log(st);

st.addEventListener('change', onSearchTextChange);

function onSearchTextChange(){
	var comment = document.querySelector('#search_comment');
	var t = st.textContent
	if (s1.value === 'delete_selected' ){
		b1.hidden = false;
		b2.hidden = true;
		i3.hidden = true;
		b1.textContent = 'Удалить';	 }
	else if(s1.value==='move_to_department'){
		//b1.hidden = true;
		i3.hidden = false;
		
		b1.textContent = 'Перевести';
		
		
	}

}




