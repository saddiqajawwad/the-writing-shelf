document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------------------
    // 1. Flash messages
    // -----------------------------------------

    const flashMessages = document.querySelectorAll(".flash-message");

    flashMessages.forEach(function (message) {

        setTimeout(function () {
            message.style.opacity = "0";
            message.style.transform = "translateY(-8px)";

            setTimeout(function () {
                message.remove();
            }, 300);

        }, 3000);

    });


    // -----------------------------------------
    // 2. Character counter for story writing
    // -----------------------------------------

    const contentBox = document.querySelector("#content");
    const characterCount = document.querySelector("#character-count");

    if (contentBox && characterCount) {

        function updateCharacterCount() {

            const length = contentBox.value.length;

            characterCount.textContent =
                length + " characters";
        }

        contentBox.addEventListener("input", updateCharacterCount);

        updateCharacterCount();
    }


    // -----------------------------------------
    // 3. Small interaction for buttons
    // -----------------------------------------

    const buttons = document.querySelectorAll(".primary-button");

    buttons.forEach(function (button) {

        button.addEventListener("click", function () {

            button.classList.add("button-clicked");

            setTimeout(function () {
                button.classList.remove("button-clicked");
            }, 180);

        });

    });

});