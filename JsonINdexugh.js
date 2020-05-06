let canvas = document.getElementById("datingsim");
let ctx = canvas.getContext('2d');
const GAME_WIDTH = 800;
const GAME_HEIGHT = 600;

var initialState = {
	progressDictionary : {
		character: 0,
		progress: 0,
		text: 0,
		letter: 1,
		option_keeper: null,
		love_meter: 0,
		json_progress: ["introduction", "1", "2"]
	},
	date: Date.now(),
	special: {"ENTER NAME": "off", "INTRO": "on", "OPTION": "off"},
	background: "casual",
	allDialogue: {
		Normal: {character: [["Mercy"]] , emotion: [["Default"]] , txt: [["Hello there"]] },
		Good: {character: [] , emotion: [] , txt:[] }, 
		Bad: {character:[] , emotion:[] , txt:[] }, 
		Neutral: {character:[] , emotion:[] , txt: []}
	},
	option: {G: "good" , N: "neutral", B: "bad", C: "Mercy"},
	mc: "Unknown",
	changex: [0, -150],
	typing: [],
	love_interest:{
    	"mainscreen": {"main":["char1Default",-150, 210]
    	},
    	"Mercy":{
    		"Default": ["char1Default",170, 40],
     		"Normal": ["char1Normal",350, 40, 600, 500], 
     		"Angry": ["char1Angry", 170, 40],
     		"Action": ["char1Action", 170, 30],
     		"Badass": ["char1Badass", 350, 40, 400,300]
     	},
    	"Unknown": {
    		"Default": ["transparent", 0,0]
    	},
    	"Nava" :{
    		"Default":["char2Default", 350, 40, 370,600]
    	}
	},
    button: {
    	"Textbox": ["textbox",90,370,600,210],
    	"Option" : ["option", 450, 80, "20px overwatch"],
    	"Start" : ["start", 125, 55, "40px bignoodle"]
   	}
};

$.getJSON("http://localhost:63342/basics/public/json/story.json", function(json) {
    start(json); 
});

function start(json) {
	var currentState = initialState;
	currentState['json'] = json;
	inputHandler(currentState);
	
	function gameLoop(timestamp) {
		ctx.clearRect(0,0, GAME_WIDTH, GAME_HEIGHT);
		
		draw(currentState, ctx);

		requestAnimationFrame(gameLoop);
	};	
	requestAnimationFrame(gameLoop);
};

function inputHandler(state){
	document.addEventListener("keydown", event => {
		if((event.keyCode == 39) || (event.keyCode >= 65 && event.keyCode <= 90) || event.keyCode == 13){
			if( event.keyCode == 39){
				if(state["special"]["INTRO"] == "off" && state["allDialogue"]["Normal"]["txt"][state["progressDictionary"]["character"]] != "ENTER NAME"){
					update(state, 39);
				}
			} else if (event.keyCode >= 65 && event.keyCode <= 90){
			 	if (state["allDialogue"]["Normal"]["txt"][state["progressDictionary"]["character"]] == "ENTER NAME"){
			 		// state["special"]["ENTER NAME"] = "on";
					var letter = String.fromCharCode(event.keyCode);
					if(state["typing"].length < 11){
						state["typing"].push(letter);
					}
					// console.log(state["txt"][state["progressDictionary"]["character"]]);
				}
			} else if (event.keyCode == 13){
				if (state["allDialogue"]["Normal"]["txt"][state["progressDictionary"]["character"]] == "ENTER NAME"){
					// state["mc"] = name;	
					update(state, 39);
					console.log("help me");
				}
			}
		}
	});
};


 function getMousePosition(canvas, event) { 
            let rect = canvas.getBoundingClientRect(); 
            let x = event.clientX - rect.left; 
            let y = event.clientY - rect.top; 
            // console.log("Coordinate x: " + x,  
            //             "Coordinate y: " + y); 
            return([x,y]);
}; 


function newGameButton(button ,state, ctx, x, y, tx, ty, txt, type){
	var Button = state["button"][button],
		newGameButton = document.getElementById(Button[0]),
		x_len = Button[1], 
		y_len = Button[2];

	ctx.drawImage(newGameButton,x,y, x_len, y_len);
	ctx.font = Button[3];
	ctx.fillStyle = "black";
	ctx.fillText(txt, tx, ty);

	let canvasElem = document.querySelector("canvas");  
    var um = canvasElem.addEventListener("mousedown", function(e) { 
    var isThisworking = getMousePosition(canvasElem, e),
    	mos_x = isThisworking[0],
    	mos_y = isThisworking[1];
    	if (mos_x > x && (mos_x < x + x_len)){
    		var x_inside = true;
    	} else {
    		var x_inside = false;
    	};
    	if (mos_y > y && (mos_y < y + y_len)){
    		var y_inside = true;
    	} else {
    		var y_inside = false;
    	};
  		if (x_inside && y_inside){
  			if (type == "good" && state["special"]["OPTION"] == "on"){
  				state["progressDictionary"]["option_keeper"] = 1;
  				state["special"]["OPTION"] = "good";
  			} else if (type == "bad" && state["special"]["OPTION"] == "on"){
  				state["progressDictionary"]["option_keeper"] = -1;
  				state["special"]["OPTION"] = "bad";
  			} else if (type == "neutral" && state["special"]["OPTION"] == "on"){
  				state["progressDictionary"]["option_keeper"] = 0;
  				state["special"]["OPTION"]= "neutral";
  			} else if (state["special"]["INTRO"] == "on"){
  				state["changex"][0] = 16; // change back to 10
  			};
    		return true;
    	};
    }); 
};


function update(state, action){
	if (action === 39){
		// general
		var date_now = Date.now();
		var json = state['json'];
		var progress = state["progressDictionary"]["json_progress"][state["progressDictionary"]["progress"]];
		var scene = json[progress][0];
		state["background"] = scene["Background"];

		state["option"]["G"] = scene["Button"][0];
		state["option"]["B"] = scene["Button"][1];
		state["option"]["N"] = scene["Button"][2];


		var charArray = [];
		var emoArray =[];
		var dialArray =[];
		var element;

		var elementxt = scene["Character"];

		for (element in elementxt){
			var dialogue = elementxt[element];
			charArray.push(dialogue[0]);
			emoArray.push(dialogue[1]);
			dialArray.push(dialogue.slice(2));
		};
		
		state["allDialogue"]["Normal"]["character"] = charArray;
		state["allDialogue"]["Normal"]["emotion"] = emoArray;
		state["allDialogue"]["Normal"]["txt"] = dialArray;

		charArray = [];
		emoArray = [];
		dialArray = [];

		var good = scene["Endings"]["Good"]["Character"];
		var neutral = scene["Endings"]["Neutral"]["Character"];
		var bad = scene["Endings"]["Bad"]["Character"];

		for (element in good){
			var dialogue = good[element];
			charArray.push(dialogue[0]);
			emoArray.push(dialogue[1]);
			dialArray.push(dialogue.slice(2));
		};

		state["allDialogue"]["Good"]["character"] = charArray;
		state["allDialogue"]["Good"]["emotion"] = emoArray;
		state["allDialogue"]["Good"]["txt"] = dialArray;
		charArray = [];
		emoArray = [];
		dialArray = [];

		for (element in neutral){
			var dialogue = neutral[element];
			charArray.push(dialogue[0]);
			emoArray.push(dialogue[1]);
			dialArray.push(dialogue.slice(2));
		};

		state["allDialogue"]["Neutral"]["character"] = charArray;
		state["allDialogue"]["Neutral"]["emotion"] = emoArray;
		state["allDialogue"]["Neutral"]["txt"] = dialArray;
		charArray = [];
		emoArray = [];
		dialArray = [];

		for (element in bad){
			var dialogue = bad[element];
			charArray.push(dialogue[0]);
			emoArray.push(dialogue[1]);
			dialArray.push(dialogue.slice(2));
		};

		state["allDialogue"]["Bad"]["character"]= charArray;
		state["allDialogue"]["Bad"]["emotion"]= emoArray;
		state["allDialogue"]["Bad"]["txt"] = dialArray;

		var txtState = state["progressDictionary"]["text"];
		var charState = state["progressDictionary"]["character"];

		//normal text length
		// var txts = 'txt';
		// var characters = "character";

		var stateID = "Normal";

		if(state["special"]["OPTION"] == "good"){
		 	stateID = "Good";
		} else if (state["special"]["OPTION"] == "bad"){
			stateID = "Bad";
		} else if (state["special"]["OPTION"] == "neutral"){
			stateID = "Neutral";
		};
		
		var txtlength = (state["allDialogue"][stateID]["txt"][charState].length -1);
		var charlength = (state["allDialogue"][stateID]["character"].length -1);



		// var txtlength = (state[txts][charState].length -1);
		// var charlength = (state[characters].length -1);

		// var tempArraytxt = [];
		// for (element in state[txts][charState]){
		// 	if (state[txts][charState][element] == "*"){
		// 		tempArraytxt.push(state["mc"]);
		// 	} else {
		// 		tempArraytxt.push(state[txts][charState][element]);
		// 	}
		// }
		// state[txts][charState] = tempArraytxt.join("");

		console.log(state);

		if(txtState < txtlength && state["special"]["OPTION"] != "on") { // fuck 
			state["progressDictionary"]["text"]++;
			state["progressDictionary"]["letter"] = 1;
			console.log(state["special"]["OPTION"] + ": " + txtState + " lessthan " + txtlength);
		} else if (txtState == txtlength && charState < charlength
			&& state["special"]["OPTION"]!= "on"){ // fuck
			state["progressDictionary"]["text"] = 0;
			state["progressDictionary"]["character"]++;
			state["progressDictionary"]["letter"] = 1;
			console.log(state["special"]["OPTION"] + ": " + txtState + " equals " + txtlength);
			console.log(charState + " less than " + charlength);
		} else if (txtState == txtlength && charState == charlength
			&& state["special"]["OPTION"] == "off"){
			state["progressDictionary"]["text"] = 0;
			state["progressDictionary"]["character"] = 0;
			state["progressDictionary"]["letter"] = 1;
			state["special"]["OPTION"] = "on";
			console.log("MADE IT HERE");
			console.log(state["special"]["OPTION"]);
			console.log(state["special"]["OPTION"] + ": " + txtState + " equals " + txtlength);
		} else if (txtState == txtlength && charState == charlength
			&& (state["special"]["OPTION"] == "bad" || state["special"]["OPTION"] == "good" || state["special"]["OPTION"] == "neutral" )){
			console.log("MADE IT OVER HERE");
			state["progressDictionary"]["text"] = 0;
			state["progressDictionary"]["character"] = 0;
			state["progressDictionary"]["letter"] = 1;
			state["progressDictionary"]["love_meter"] = state["progressDictionary"]["love_meter"] + state["progressDictionary"]["option_keeper"];
			state["progressDictionary"]["progress"] ++;
			state["special"]["OPTION"] = "off";
			console.log(state["progressDictionary"]["love_meter"]);
		} else {
			console.log("you fucked up");
		};

	}
};


function draw(state, ctx){
	if (state["special"]["INTRO"] == "on"){
			gameIntro(ctx, state);	
	} else {
		// console.log(state["special"]["OPTION"]);
		var love_interest = state["love_interest"];
		var miniProgress = state["progressDictionary"]["character"];
		var txtProgress = state["progressDictionary"]["text"];
		var txt_len = state["progressDictionary"]["letter"];
		var currentButton = state["button"]["Textbox"];

		var	currentID = "Normal";

		if (state["special"]["OPTION"] == "good"){
			currentID = "Good"; 
		} else if (state["special"]["OPTION"]== "bad"){
			currentID = "Bad";
		} else if (state["special"]["OPTION"] == "neutral"){
			currentID = "Neutral";
		};

		var currentCharID = state["allDialogue"][currentID]["character"][miniProgress];
		var currentEmo = state["allDialogue"][currentID]["emotion"][miniProgress];
		// console.log(state["allDialogue"][currentID]["emotion"] + state["progressDictionary"]["progress"]);
		var currentChar = love_interest[currentCharID][currentEmo];
		var miniMinitxt = (state["allDialogue"][currentID]["txt"][miniProgress][txtProgress].length);
		// var currentChar = love_interest[currentCharID][currentEmo];

		//draws background
		var bgImage = document.getElementById(state["background"]);
		ctx.drawImage(bgImage, 0,0);

		//draws character
		var charImage = document.getElementById(currentChar[0]);
		if (currentChar.length == 5){
			ctx.drawImage(charImage, currentChar[1], currentChar[2], currentChar[3], currentChar[4]);
		} else{
			ctx.drawImage(charImage, currentChar[1],currentChar[2]);
		};

		if (state["special"]["OPTION"] != "on") {
			//draws the text
			var txtImage = document.getElementById(currentButton[0]);
			ctx.fillStyle = "#FFF6F6";
			ctx.fillRect(123,407,534,135);
			ctx.drawImage(txtImage, currentButton[1], currentButton[2], currentButton[3], currentButton[4]);

			//character title on txtbox
			ctx.font = "25px bignoodle";
			ctx.fillStyle = "#D291BC";
			if (currentCharID == "Unknown"){
				ctx.fillText(state["mc"], 150, 430);
			} else{
				ctx.fillText(currentCharID, 150, 430);
			};

			//text on screen
			ctx.font = "20px overwatch";
			ctx.fillStyle = "#2A1D26";

			state["date"] = Date.now();

			// state["txt"]state["progressDictionary"]["character"] == "ENTER NAME";
			// console.log(state["txt"][state["progressDictionary"]["character"]][0][state["progressDictionary"]["letter"]]);

			if(state["allDialogue"][currentID]["txt"][miniProgress] == "ENTER NAME"){
				ctx.drawImage(bgImage, 0,0);
				// state["special"]["ENTER NAME"] = "on";
				ctx.fillStyle = "#D291BC";
				ctx.fillRect(265, 227, 250, 50);
				ctx.font = "25px overwatch";
				ctx.fillStyle = "white";
				ctx.fillText("Name: ", 270, 260);
				if (state["typing"].length > 0){
					var joining = state["typing"].join("");
					var name = joining[0] + joining.slice(1).toLowerCase();
					ctx.fillText(name, 345, 260);
					state["mc"] = name;	
				}
				console.log(name);
			};

			if(state["progressDictionary"]["letter"] < miniMinitxt && (state["date"] + 1000) >= Date.now()){
				state["date"] = Date.now();
				state["progressDictionary"]["letter"]++;
				var blittxtonscreen = state["allDialogue"][currentID]["txt"][miniProgress][txtProgress].slice(0,txt_len);
				ctx.fillStyle = "black"; 
				ctx.fillText(blittxtonscreen,160, 470);
			} else if (state["progressDictionary"]["letter"] == miniMinitxt){
				ctx.fillStyle = "black";
				ctx.fillText(state["allDialogue"][currentID]["txt"][miniProgress][txtProgress], 160, 470);
				state["date"] = Date.now();
			};	
		} else if (state["special"]["OPTION"] == "good" || state["special"]["OPTION"] == "bad" || state["special"]["OPTION"] == "neutral"){
		
			ctx.drawImage(bgImage, 0,0);
			var txtImage = document.getElementById(currentButton[0]);
			ctx.fillStyle = "#FFF6F6";
			ctx.fillRect(123,407,534,135);
			ctx.drawImage(txtImage, currentButton[1], currentButton[2], currentButton[3], currentButton[4]);

			//character on screen
			ctx.font = "25px bignoodle";
			ctx.fillStyle = "#D291BC";

			// if (state["special"]["OPTION"] == "good"){
			// 	currentCharID = love_interest[state["allDialogue"]["Good"]["character"][0][1]]; // make
			// 	tempText = state["goodchoice"][2]; // make

			// 	ctx.fillText("Unknown", 150, 430);

			// 	//text on screen
			// 	ctx.font = "20px overwatch";
			// 	ctx.fillStyle = "#2A1D26";
			// 	var miniMinitxt = (tempText.length);
			// };
			state["date"] = Date.now();

			if(state["progressDictionary"]["letter"] < miniMinitxt && (state["date"] + 1000) >= Date.now()){
				state["date"] = Date.now();
				state["progressDictionary"]["letter"]++;
				var blittxtonscreen = tempText.slice(0,txt_len);
				ctx.fillStyle = "black"; 
				ctx.fillText(blittxtonscreen,160, 470);
			} else if (state["progressDictionary"]["letter"] == miniMinitxt){
				ctx.fillStyle = "black";
				ctx.fillText(tempText, 160, 470);
				state["date"] = Date.now();
			};	

		} else if(state["special"]["OPTION"] == "on"){
			newGameButton("Option", state, ctx, 50, 120, 100, 160, state["option"]["G"], "good");
			newGameButton("Option", state, ctx, 50, 220, 100, 260, state["option"]["B"], "bad");
			newGameButton("Option", state, ctx, 50, 320, 100, 360, state["option"]["N"], "neutral");

		} else {
			console.log("fuck it up fuck it up");

		}
	}
};


function gameIntro(ctx, state){
	var bgImage = document.getElementById("default");
	ctx.drawImage(bgImage, 0,0);
	ctx.fillStyle = "#D291BC";
	ctx.fillRect(257,25,264,60);
	ctx.font = "46px bignoodle";
	ctx.fillStyle = "white";
	ctx.fillText("Mercy Dating Sim!", 260, 70);	
	var charImage = document.getElementById("char1Default");
	ctx.drawImage(charImage, state["changex"][1], 210);
	newGameButton("Start", state, ctx, 330, 90, 353, 135, "START", "intro");
	if (state["changex"][1] < 600){
		ctx.drawImage(bgImage, 0,0 );
		ctx.fillStyle = "#D291BC";
		ctx.fillRect(257,25,264,60);
		ctx.font = "46px bignoodle";
		ctx.fillStyle = "white";
		ctx.fillText("Mercy Dating Sim!", 260, 70);		
		ctx.drawImage(charImage, state["changex"][1], 210);
		newGameButton("Start", state, ctx, 330, 90, 353, 135, "START", "intro");
		state["changex"][1] = state["changex"][1] + state["changex"][0];
	} else if (state["changex"][1] >= 600){
		state["special"]["INTRO"] = "off";
	};
};


function typeBox(state, question, typing){
	if (state["special"]["ENTER NAME"] == "on"){
		if(state["typing"].length < 11){
			state["typing"].push(typing);
		}
	}
};