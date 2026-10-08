console.log("test");
let scriptEle = document.createElement("script");
scriptEle.setAttribute("src", "https://codio.com/codio-client.js");
scriptEle.setAttribute("type", "text/javascript");

document.body.appendChild(scriptEle);

document.getElementById("runBtn").addEventListener("click", runCode);
document.getElementById("stopBtn").addEventListener("click", stopCode);
document.getElementById("clearBtn").addEventListener("click", clearCode);

		function runCode(){
			codio.open("terminal","python3 Main.py",1 );
		}

		// Stop the running program (terminal shows "Terminated"), without closing any tabs.
		// [M]ain stops pkill from matching (and killing) its own command.
		// done() is called once the program has been stopped.
		function stopCode(done){
			let finished = false;
			function finish(){
				if (!finished && typeof done === "function"){
					finished = true;
					done();
				}
			}
			codio.run('pkill -f "python3 [M]ain.py"', finish);
			// in case Codio doesn't call back, continue anyway
			setTimeout(finish, 500);
		}

		// Stop the program first, otherwise "clear" is typed into the program's input()
		function clearCode(){
			stopCode(function(){
				codio.open("terminal","clear");
			});
		}

// Keep Check It! sections open after Codio redraws them with new results.
// Remembers which sections the student opened, then reopens them.
const openSections = {};
document.addEventListener("toggle", function(e){
	const box = e.target.closest ? e.target.closest(".codio-assessment-test") : null;
	if (box && e.target.tagName === "DETAILS"){
		openSections[box.getAttribute("aria-labelledby")] = e.target.open;
	}
}, true);
new MutationObserver(function(){
	document.querySelectorAll(".codio-assessment-test").forEach(function(box){
		const section = box.querySelector(".codio-assessment-instructions details");
		if (section && !section.open && openSections[box.getAttribute("aria-labelledby")]){
			section.open = true;
		}
	});
}).observe(document.body, {childList: true, subtree: true});
