const estesC6 = {
    name: "Estes C6-5 Motor",
    type: "motor",
    thrust: 15.3,
    burn_time: 1.6,
    propellant_mass: 0.011,
    price: 18.94,
    link: "https://estesrockets.com/products/c6-5-engines?_pos=2&_sid=019f2ac47&_ss=r",
    description: "The C6-5 is the go-to starter motor for first flights. It burns for 1.6 seconds and will send a typical beginner rocket over 300 meters, which is about the height of the Eiffel Tower."
}

const estesBT50 = {
    name: "Estes BT-50 Body Tube",
    type: "body_tube",
    diameter: 0.022,
    length: 0.4572,
    mass: 0.025,
    price: 12.90,
    link: "https://estesrockets.com/products/bt-50-body-tube?_pos=8&_sid=ffd4a9069&_ss=r",
    description: "The BT-50 is a high-quality body tube designed for durability and precision. It's perfect for building sturdy rockets that can withstand the rigors of flight."
}

const estesNC50 = {
    name: "Estes NC-50 Nose Cone Pack",
    type: "nose_cone",
    diameter: 0.02413,
    length: 0.09525,
    mass: 0.008,
    material: "ABS Plastic",
    compatible_tube: "BT-50",
    price: 9.99,
    link: "https://estesrockets.com/products/nc-50-nose-cone-5-pk?_pos=1&_sid=33efdc7e0&_ss=r",
    description: "Lightweight ABS plastic nose cone designed for BT-50 body tubes. Aerodynamic profile reduces drag and the integrated shoulder locks it in place securely."
}

const estesParachute = {
    name: "Estes 12-inch Parachute",
    type: "parachute",
    diameter: 0.3048,
    cd: 0.75,
    mass: 0.015,
    price: 5.49,
    link: "https://estesrockets.com/products/12-inch-printed-parachute?_pos=2&_sid=199735ea6&_ss=r",
    description: "Standard 12-inch plastic parachute. Slows your rocket to a safe landing speed under 6 m/s. Fits most beginner rockets."
}

const parts = [estesC6, estesBT50, estesNC50, estesParachute];