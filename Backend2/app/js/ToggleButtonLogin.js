import React, { useState} from 'react';
import './Toggle-container.css';

function  ToggleButtons() {
    const [activeButton, setActiveButton] = useState('phone');
    
    const handleButtonClick = (buttonName) => {
        setActiveButton(buttonName);
    };

    return (
        <div className="toggle-button">
            <button
                const phoneButton = document.getElementById("phone-button");
                const emailButton = document.getElementById("email-button");
            
                phoneButton.addEventListener("click", () => {
                    phoneButton.classList.add("active");
                    emailButton.classList.remove("active");
                });
            
                emailButton.addEventListener("click", () => {
                    emailButton.classList.add("active");
                    phoneButton.classList.remove("active");
                });
            >
            </button>    
        </div>
    )
        

