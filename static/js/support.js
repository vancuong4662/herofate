//////--- (START) Các function hỗ trợ ---//////

// Hàm chuyển thời gian timestring về timestamp :
const convertToTimestamp = (timeString) => {
    // Tách thông tin về ngày, tháng, năm, giờ, phút, giây và AM/PM từ chuỗi
    const [, day, month, year, time] = timeString.match(/(\d+)\/(\d+)\/(\d+), (.+)/);

    // Tạo một đối tượng Date từ thông tin đã tách
    const dateObject = new Date(`${month}/${day}/${year} ${time}`);

    // Lấy timestamp từ đối tượng Date
    const timestamp = dateObject.getTime();

    return timestamp;
};

// Hàm để tự động lấy thời gian hiện tại :
const getCurrentTimeDate = () => {
    const currentDate = new Date();
    const day = currentDate.getDate();
    const month = currentDate.getMonth() + 1; // Tháng trong JavaScript bắt đầu từ 0, nên cần cộng thêm 1
    const year = currentDate.getFullYear();

    // Tạo chuỗi ngày/tháng/năm
    const dateString = `${day}/${month}/${year}`;
    const timeString = currentDate.toLocaleTimeString();
    const dateTimeString = `${dateString}, ${timeString}`;
    return dateTimeString;
};

const getCurrentTimeDateString = () => {
    const currentDate = new Date();
    const day = String(currentDate.getDate()).padStart(2, '0');
    const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Tháng trong JavaScript bắt đầu từ 0, nên cần cộng thêm 1
    const year = currentDate.getFullYear();
    const hours = String(currentDate.getHours()).padStart(2, '0');
    const minutes = String(currentDate.getMinutes()).padStart(2, '0');
    const seconds = String(currentDate.getSeconds()).padStart(2, '0');

    // Tạo chuỗi ngày-tháng-năm và giờ-phút-giây
    const dateString = `${year}-${month}-${day}`;
    const timeString = `${hours}:${minutes}:${seconds}`;
    const dateTimeString = `${dateString}T${timeString}`;
    return dateTimeString;
};

const formatTime = (time) => {
    // Định dạng của biến time sẽ có dạng "2024-10-25T22:58:47"
    // Format time to "YYYY-MM-DD HH:MM:SS"
    const date = new Date(time);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;  
    const day = date.getDate();
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
    const second = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
};


// Xếp lại POST LIST MAP theo thứ tự thời gian từ mới nhất
const sortLastestByTimestamp = (list) => {
    // Sắp xếp mảng theo giá trị timestamp giảm dần
    // Timestamp càng lớn nhất, thì thời gian càng mới nhất
    list.sort((a, b) => b.timestamp - a.timestamp);

    return list;
};

// Xáo trộn ngẫu nhiên các phần tử với một Array
const shuffleArray = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        // Swap array[i] and array[j]
        [array[i], array[j]] = [array[j], array[i]]; // Toán tử destructuring assignment
    }
    return array;
};

// Tải một hình ảnh với URL và trả về một Promise:
const loadAsyncImageFromUrl = async (url) => {
    return new Promise((resolve, reject) => {
        const image = new Image();
        image.src = url;
        image.onload = () => {
            // Nếu hình ảnh tải thành công, resolve Promise
            resolve(image);
        };
        image.onerror = () => {
            // Nếu có lỗi trong quá trình tải hình ảnh, reject Promise
            console.error("Lỗi", "Không tải được hình ảnh từ : " + url);
            reject(new Error("Không tải được hình ảnh từ : " + url));
        };
    });
};

// Tải động một hình ảnh từ URL :
const loadDynamicImage = (url, callback) => {
    const image = new Image();
    image.src = url;
    image.onload = () => {
        callback(image);
    };
    image.onerror = () => {
        console.error("Lỗi", "Không tải được hình ảnh từ : " + url);
        callback(image);
    };
};

// Gán innerHTML cho tất cả Element có chung class :
const setInnerHTMLByClasseName = (className, innerHTMLContent) => {
    const elementList = document.querySelectorAll(`.${className}`);
    elementList.forEach((eachElement) => {
        eachElement.innerHTML = innerHTMLContent;
    });
};

// Hàm promise ghi dữ liệu vào localStorage :
const setLocalStorage = (key, value) => {
    return new Promise((resolve, reject) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            resolve();
        } catch (error) {
            reject(error);
        }
    });
}

// Hàm clear và gán dữ liệu mới cho một constant object :
const clearAndAssignObject = (object, newData) => {
    Object.keys(object).forEach(key => delete object[key]);
    Object.assign(object, newData);
};

// Chuyển đổi đường dẫn tệp cục bộ thành đường dẫn URL tương đối
const getRelativePath = (fullPath, basePath) => {
    return fullPath.replace(basePath, '').replace(/\\/g, '/');
}

// Hàm quy đổi tiếng việt không dấu :
const convertVietnameseNoSpecial = (str) => {
    str = str.toLowerCase();
    str = str.replace(/á|à|ả|ã|ạ|ă|ắ|ằ|ẳ|ẵ|ặ|â|ấ|ầ|ẩ|ẫ|ậ/g, 'a');
    str = str.replace(/đ/g, 'd');
    str = str.replace(/é|è|ẻ|ẽ|ẹ|ê|ế|ề|ể|ễ|ệ/g, 'e');
    str = str.replace(/í|ì|ỉ|ĩ|ị/g, 'i');
    str = str.replace(/ó|ò|ỏ|õ|ọ|ô|ố|ồ|ổ|ỗ|ộ|ơ|ớ|ờ|ở|ỡ|ợ/g, 'o');
    str = str.replace(/ú|ù|ủ|ũ|ụ|ư|ứ|ừ|ử|ữ|ự/g, 'u');
    str = str.replace(/ý|ỳ|ỷ|ỹ|ỵ/g, 'y');
    return str;
};

// Hàm lấy ngẫu nhiên một thời gian trong vòng số tháng trở lại đây
const getRandomTimeInLastMonths = (months) => {
    const now = new Date();
    const pastDate = new Date();
    pastDate.setMonth(now.getMonth() - months);

    const randomTime = new Date(pastDate.getTime() + Math.random() * (now.getTime() - pastDate.getTime()));
    const year = randomTime.getFullYear();
    const month = String(randomTime.getMonth() + 1).padStart(2, '0'); // Tháng trong JavaScript bắt đầu từ 0, nên cần cộng thêm 1
    const day = String(randomTime.getDate()).padStart(2, '0');
    const hours = String(randomTime.getHours()).padStart(2, '0');
    const minutes = String(randomTime.getMinutes()).padStart(2, '0');
    const seconds = String(randomTime.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};