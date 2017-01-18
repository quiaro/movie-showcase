/*
 * @class
 * Coverflow display from an array of images
 *
 * Based on the work by Joseph Khan:
 * https://jbkflex.wordpress.com/2012/02/13/coverflow-animation-using-css3-3d-transformations-part1/
 *
 * @param {string[]} elId - DOM id of the element to which attach the coverflow functionality (defaults to 'coverflow')
 * @param {Object} options - Options that control the appearance and behaviour of the
 *                           Coverflow instance.
 * @property {number}  options.angleInactive  - Degrees of rotation for all inactive images
 * @property {number}  options.centerGap  - Pixel gap between the center image and the images next to it
 * @property {number}  options.current    - Image index to display as active by default
 * @property {number}  options.gap        - Pixel gap between images
 * @property {number}  options.zActive    - Number of pixels that the active image will appear closer (z translation)
 */
function Coverflow(elId, options) {

    let root = document.getElementById(elId);

    if (!root) {
        console.error(`Element #${elId} not found. Unable to initialize coverflow display.`);
        return;
    }

    this.root = root;
    this.images = root.getElementsByTagName('img');

    if (!this.images.length) {
        console.error(`No images found in element #${elId}. Unable to initialize coverflow display.`);
        return;
    }

    // Instance default option values
    var defaults = {
        angleInactive: 70,
        centerGap: 120,
        current: Math.floor(this.images.length / 2), // The middle image will be set to display by default
        gap: 30,
        zActive: 200
    };

    this.settings = Object.assign({}, defaults, options);
    console.info(`New instance of coverflow display with ${this.images.length} images`);
    console.info('Coverflow settings: ', this.settings);
}

/*
 * @method getCurrentImage
 * Get reference to image currently selected (zero-indexed)
 */
Coverflow.prototype.getCurrentImage = function() {
    return this.images[this.settings.current];
}

/*
 * @method getCurrent
 * Get index to the currently selected image (zero-indexed)
 */
Coverflow.prototype.getCurrentIndex = function() {
    return this.settings.current;
}

/*
 * @method init
 * Initial display of images. Animate scroll to the image currently selected.
 */
Coverflow.prototype.init = function() {
    let images = this.images;
    let current = this.settings.current;

    // Temporarily set the current image to -1 to show all
    // images in a starting position
    this.settings.current = -1;

    for (let i = images.length - 1; i >= 0; i--) {
        this.updatePosition(i);
    }

    // Delay before showing the images in their starting position
    setTimeout(() => {
        this.root.className += 'plugin-coverflow';

        if (current >= 0 && current < images.length) {
            // Short delay before presenting the images in their actual position
            // (per the settings.current value). If value of settings.current is out
            // of bounds, then settings.current is left with a value of -1.
            setTimeout(() => {
                this.settings.current = current;
                for (let i = images.length - 1; i >= 0; i--) {
                    this.updatePosition(i);
                }
            }, 500);
        }
    }, 500);
}

/*
 * @method moveTo
 * @param {number} numIndex
 *
 * Sets the image at a specific index as current
 */
Coverflow.prototype.moveTo = function(numIndex) {
    let len = this.images.length;
    this.settings.current = numIndex;

    for (let i = 0; i < len; i++) {
        this.updatePosition(i);
    }
};

/*
 * @method updatePosition
 * @param {number} imgIdx - Index of the image to be updated
 *
 * Calculate the position and the angle of an image relative to the image
 * currently selected.
 */
Coverflow.prototype.updatePosition = function(imgIdx) {
    let settings = this.settings;

    // Distance from image[i] to the current image
    let dist = Math.abs(imgIdx - settings.current);

    if (dist) {
        let newPos = settings.gap * (dist - 1) + settings.centerGap;
        let newAngle = settings.angleInactive;

        newPos = (imgIdx < settings.current)
            ? newPos *= -1
            : newPos;
        newAngle = (imgIdx > settings.current)
            ? newAngle *= -1
            : newAngle;
        this.updateInDom(imgIdx, false, newPos, newAngle);
    } else {
        // image[i] is the current image
        this.updateInDom(imgIdx, true);
    }
}

/*
 * @method updateInDom
 * @param {number} imgIdx   - Index of the image to be updated
 * @param {number} isActive - Is this the currently selected image?
 * @param {number} newPos   - Translate X value of the image
 * @param {number} newAngle - Rotate Y value of the image
 *
 * Refresh the inline styles of an image in the DOM
 */
Coverflow.prototype.updateInDom = function(imgIdx, isActive, newPos, newAngle) {
    let settings = this.settings;

    if (isActive) {
        this.images[imgIdx].setAttribute('style', `transform: translateX(0) rotateY(0deg) translateZ(${settings.zActive}px)`);
    } else {
        this.images[imgIdx].setAttribute('style', `transform: translateX(${newPos}px) rotateY(${newAngle}deg)`);
    }
}
