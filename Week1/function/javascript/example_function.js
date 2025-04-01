exports.handler = async (event) => {
    return { message: "Hello from JavaScript!" };
};

if (require.main === module) {
    console.log(exports.handler({}));
}