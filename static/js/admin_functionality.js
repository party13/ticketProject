
jQuery('document').ready(function(){

    console.log('loaded newFunctionality');
    //var f1 = document.querySelector('.actions');
    var s1 = document.querySelector('.actions select');
    var b1 = document.querySelector('.actions button');
    var i3 = document.createElement('select');
    var b2 = document.createElement('button');
    b2.hidden = true;
    i3.hidden = true;
    document.querySelector('.actions').appendChild(i3);
    //f1.appendChild(b2);

    s1.addEventListener('change', onActionChange);

    function onActionChange(){
        //var s1 = f1.querySelector('select');
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

});

