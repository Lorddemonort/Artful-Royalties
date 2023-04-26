// Get the generate button
const generateBtn = document.getElementById("generate-btn");

// Get the prompt input
const promptInput = document.getElementById("prompt");

// Get the generated image element
const generatedImage = document.getElementById("generated-image");

// Get the loader element
const loader = document.getElementById("loader");

// Get the credits element
const credits = document.getElementById("credits");

// Set the initial credits
let remainingCredits = 100;
credits.textContent = remainingCredits;

// Attach click event listener to generate button
generateBtn.addEventListener("click", () => {
	// Decrement the credits
	if (remainingCredits > 0) {
		remainingCredits--;
		credits.textContent = remainingCredits;
	} else {
		alert("You do not have enough credits!");
		return;
	}
	
	// Get the prompt
	const prompt = promptInput.value;
	
	// Show the loader
	loader.classList.remove("d-none");
	
	// Generate the image
	const imageUrl = `https://picsum.photos/800/600/?${prompt}`;
	generatedImage.src = imageUrl;
	
	// Hide the loader
	generatedImage.onload = () => {
		loader.classList.add("d-none");
	};
});
