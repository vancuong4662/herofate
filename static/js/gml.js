let instGlobalList = []; // Mảng toàn cục chứa tất cả các instance
let instIdCounter = 0; // Biến đếm để tạo ID duy nhất cho mỗi instance
let sprites = []; // Mảng chứa tất cả sprite
let sortInstFlag = false; // Cờ để kiểm tra xem đã sắp xếp các instance theo depth chưa
let mouseX = 0; // Lưu tọa độ X của chuột
let mouseY = 0; // Lưu tọa độ Y của chuột

//#region CALCULATION FUNCTIONS
const pointDistance = (x1, y1, x2, y2) => {
    return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
};
const pointDirection = (x1, y1, x2, y2) => {
    return Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
}
//#endregion

//#region Image Loading System
// Lưu trạng thái của từng hình ảnh
const imageStatus = new Map();  // "loading", "loaded", "error"
// Hàm preload hình ảnh với trạng thái
const preloadImageWithStatus = (url) => {
    return new Promise((resolve, reject) => {
        // Nếu ảnh đã tải xong hoặc đang tải, không cần tải lại
        if (imageStatus.get(url) === "loaded") {
            resolve(url);
            return;
        } else if (imageStatus.get(url) === "loading") {
            // Nếu đang tải, đợi nó tải xong rồi trả về
            const checkInterval = setInterval(() => {
                if (imageStatus.get(url) === "loaded") {
                    clearInterval(checkInterval);
                    resolve(url);
                } else if (imageStatus.get(url) === "error") {
                    clearInterval(checkInterval);
                    reject(`Lỗi tải ảnh: ${url}`);
                }
            }, 100);
            return;
        }

        // Đánh dấu trạng thái đang tải
        imageStatus.set(url, "loading");

        // Tạo đối tượng hình ảnh
        const img = new Image();
        img.src = url;

        img.onload = () => {
            imageStatus.set(url, "loaded");
            resolve(img);
        };

        img.onerror = () => {
            imageStatus.set(url, "error");
            reject(`Lỗi tải ảnh: ${url}`);
        };
    });
};
const isImageLoaded = (url) => {
    return imageStatus.get(url) === "loaded";
};
const preloadImageList = (urls) => {
    return Promise.all(urls.map(url => preloadImageWithStatus(url)))
        .then(() => console.log("Tất cả hình ảnh đã tải xong!"))
        .catch(err => console.error(err));
};
//#endregion

//#region SPRITE FUNCTIONS
const spriteCreate = (imageUrl, frameWidth, frameHeight, frameNumber = 1, xOrigin = 0, yOrigin = 0) => {
    const newImage = new Image();
    newImage.src = imageUrl;
    const sprite = { image: newImage, frameWidth, frameHeight, frameNumber, xOrigin, yOrigin };
    sprites.push(sprite);
    return sprite;
}
//#endregion



//#region INSTANCE FUNCTIONS
const sortInstancesByDepth = (instId, newDepth) => {
    const instance = instGlobalList.find(inst => inst.instId === instId);
    if (instance && instance.depth !== newDepth) {
        instance.depth = newDepth;
        sortInstFlag = true; // Đánh dấu cần sắp xếp lại
    }
}

const instCreate = (x, y, depth, spriteIndex) => {
    const instance = {
        instId: instIdCounter++, // Tạo ID duy nhất
        x, y, depth, spriteIndex, 
        direction: 0,
        speed: 0,
        hspeed: 0,
        vspeed: 0,
        idling: false, // ám chỉ cơ chế có dừng ở xtarger, ytarget hay không
        xtarget: x,
        ytarget: y,
        xscale: 1, // Tỉ lệ co dãn theo chiều x
        yscale: 1, // Tỉ lệ co dãn theo chiều y
        alpha: 1, // Độ trong suốt
        imageSpeed: 1, // Tốc độ chuyển frame mặc định
        imageIndex: 0, // Frame hiện tại
        imageFrameCounter: 0, // Biến đếm để chuyển frame
        imageLoop: true, // Lặp animation
        imageEnd: false, // Đã kết thúc animation hay chưa
        backgroundLoop: "none", // Instance này là background, lặp theo chiều nào
        backgroundLoopSpeed: 1, // Tốc độ lặp lại
    };
    instGlobalList.push(instance); // Thêm instance vào mảng
    sortInstFlag = true; // Đánh dấu cần sắp xếp lại các instance theo depth
    return instance; // Trả về instance vừa tạo (nếu cần)
}

const instTeleport = (instId, x, y) => {
    const instance = instGlobalList.find(inst => inst.instId === instId);
    if (instance) {
        instance.x = x;
        instance.y = y;
    }
};

const instMoveToPoint = (instId, x, y, speed) => {
    const instance = instGlobalList.find(inst => inst.instId === instId);
    if (instance) {
        // Thay đổi hspeed, vspeed để di chuyển từ inst.x, inst.y hướng tới tọa độ x, y
        instance.hspeed = speed * Math.cos((Math.atan2(y - instance.y, x - instance.x) * 180 / Math.PI) * Math.PI / 180);
        instance.vspeed = speed * Math.sin((Math.atan2(y - instance.y, x - instance.x) * 180 / Math.PI) * Math.PI / 180);
    }
};

const instMoveToPointAndStop = (instId, x, y, speed) => {
    if (!instId) {
        console.error("instMoveToPointAndStop: Instance không tồn tại!");
        return;
    }

    const instance = instGlobalList.find(inst => inst.instId === instId);
    if (!instance) {
        console.error("Instance không tìm thấy trong danh sách!");
        return;
    }
    if (instance) {
        // Thay đổi hspeed, vspeed để di chuyển từ inst.x, inst.y hướng tới tọa độ x, y
        instance.hspeed = speed * Math.cos((Math.atan2(y - instance.y, x - instance.x) * 180 / Math.PI) * Math.PI / 180);
        instance.vspeed = speed * Math.sin((Math.atan2(y - instance.y, x - instance.x) * 180 / Math.PI) * Math.PI / 180);
        // Đặt tọa độ đích
        instance.xtarget = x;
        instance.ytarget = y;
        instance.idling = true;
    }
};

const instDestroy = (instId) => {
    instGlobalList = instGlobalList.filter(inst => inst.instId !== instId); // Lọc ra instance cần xóa
};

const instExist = (instId) => {
    return instGlobalList.some(inst => inst.instId === instId); // Trả về true nếu instance tồn tại
};
//#endregion

//#region DRAWING FUNCTIONS
const drawInstances = (ctx) => {
    if (sortInstFlag) {
        sortInstancesByDepth();
        sortInstFlag = false;
    }
    instGlobalList.forEach(inst => {
        drawSprite(ctx, inst.spriteIndex, inst.imageIndex, inst.x, inst.y, inst.xscale, inst.yscale, inst.alpha);
        // Nếu instance là background và lặp lại, vẽ thêm 2 lần nữa
        if (inst.backgroundLoop === "horizontal") {
            drawSprite(ctx, inst.spriteIndex, inst.imageIndex, inst.x - inst.spriteIndex.frameWidth, inst.y, inst.xscale, inst.yscale, inst.alpha);
            drawSprite(ctx, inst.spriteIndex, inst.imageIndex, inst.x + inst.spriteIndex.frameWidth, inst.y, inst.xscale, inst.yscale, inst.alpha);
        }
        else if (inst.backgroundLoop === "vertical") {
            drawSprite(ctx, inst.spriteIndex, inst.imageIndex, inst.x, inst.y - inst.spriteIndex.frameHeight, inst.xscale, inst.yscale, inst.alpha);
            drawSprite(ctx, inst.spriteIndex, inst.imageIndex, inst.x, inst.y + inst.spriteIndex.frameHeight, inst.xscale, inst.yscale, inst.alpha);
        }
    });
};

const drawSprite = (ctx, spriteIndex, imageIndex, x, y, xscale = 1, yscale = 1, alpha = 1) => {
    const frameWidth = spriteIndex.frameWidth; // Chiều rộng của một frame
    const frameHeight = spriteIndex.frameHeight; // Chiều cao của một frame
    const xOrigin = spriteIndex.xOrigin; // Tọa độ x của gốc tọa độ
    const yOrigin = spriteIndex.yOrigin; // Tọa độ y của gốc tọa độ

    // Tính toán vị trí frame trong sprite sheet
    const sx = imageIndex * frameWidth;
    const sy = 0;
    const sw = frameWidth;
    const sh = frameHeight;

    // Lưu trạng thái hiện tại của context
    ctx.save();

    // Áp dụng các biến đổi
    ctx.translate(x, y); // Di chuyển gốc tọa độ
    ctx.scale(xscale, yscale); // Co dãn
    ctx.globalAlpha = alpha; // Độ trong suốt

    // Vẽ frame lên canvas
    ctx.drawImage(
        spriteIndex.image, // Hình ảnh sprite sheet
        sx, sy, sw, sh, // Vị trí và kích thước frame trong sprite sheet
        -xOrigin, -yOrigin, frameWidth, frameHeight // Vị trí và kích thước để vẽ lên canvas
    );

    // Khôi phục trạng thái ban đầu của context
    ctx.restore();

    // TEST : Vẽ thêm một chấm đỏ ở vị trí x y
    ctx.fillStyle = 'red';
    ctx.fillRect(x, y, 2, 2);

}
//#endregion

