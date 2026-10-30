const objects = document.querySelectorAll(".object");
        const message = document.querySelector("#game-message");

        objects.forEach((object) => {
            object.addEventListener("click", () => {
                if (object.dataset.color === "red") {
                    message.textContent = "You Win!";
                    objects.forEach((item) => {
                        item.disabled = true;
                    });
                } else {
                    message.textContent = "Not that one.";
                }
            });
        });