var _CONTENT = [
    "Jimmy's Tot Loaf",
	"Joint Tool Launcher"
];

var _PART = 0;
var _PART_INDEX = 0;
var _INTERVAL_VAL;
var itHappened = 0;

function Type() {
	var text =  _CONTENT[_PART].substring(0, _PART_INDEX + 1);
	_ELEMENT.innerHTML = text;
	_PART_INDEX++;

	if(text === _CONTENT[_PART]) {
		clearInterval(_INTERVAL_VAL);
		if(itHappened < 1){
		    setTimeout(function() {
                _INTERVAL_VAL = setInterval(Delete, 50);
            }, 1000);
		}
		else{
		    typedWords.style.display = "none";
            normalWords.style.display = "block";
		    return;
		}
	}
}

function Delete() {
	var text =  _CONTENT[_PART].substring(0, _PART_INDEX - 1);
	_ELEMENT.innerHTML = text;
	_PART_INDEX--;

	if(text === '') {
		clearInterval(_INTERVAL_VAL);

		if(_PART == (_CONTENT.length - 1))
			_PART = 0;
		else
			_PART++;

		_PART_INDEX = 0;

		setTimeout(function() {
			_INTERVAL_VAL = setInterval(Type, 100);
		}, 200);
		itHappened += 1;
	}
}
function startTypeAnimation(typedWords, normalWords, _ELEMENT){
    typedWords.style.display = "none";
    setTimeout(function(){
        typedWords.style.display = "block";
        normalWords.style.display = "none";
        _INTERVAL_VAL = setInterval(Type, 100);
    }, 60000);
}

function fadeBurger(){
    $('#burger-wrapper').on('click', function() {
        if ($('#middle-line').css('opacity') == 0){
            $('#middle-line').css('opacity', 1);
            $('.mobile-menu').toggleClass('animate-opacity-in-quick');
            $('#mobile-menu').css("display", "none");
        }
        else{
            $('#middle-line').css('opacity', 0);
            $('.mobile-menu').toggleClass('animate-opacity-in-quick');
            $('#mobile-menu').css("display", "flex");
        }

        $('.line1').toggleClass('line-rotate');
        $('.line3').toggleClass('line-rotate2');
    });
}