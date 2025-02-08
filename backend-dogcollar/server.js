const express = require("express")
const app = express()

const cors = require("cors")
const corsOptions = {
    origin: ["http://localhost:5173"],
}

app.use(cors(corsOptions))

app.get("/", (req, res) => {

    res.json({"test": ["Robbie", "Max", "Ethan"]})
})

app.listen( 8080, () => {
    console.log("Server started on port 8080.")
})

app.get("/getLatestData", (req, res) => {
    // This will get hit whenever the pico is ready to send coordinate data
    // const binaryData = req.body       this is what will be done once the transfer is actually setup, just using this part for now.
    const binaryData = Buffer.from([0x07, 0xF8, 0xA9, 0xE5, 0x28, 0xA9, 0x41, 0x22, 0x43])

    const binary = [...binaryData].map(byte => byte.toString(2).padStart(8, '0')).join('').slice(4)
    const timeBinary = binary.slice(0, 17);  // First 17 characters are time
    const latBinary = binary.slice(17, 41);  // Next 24 characters are latitude
    const latDirBinary = binary.slice(41, 42);  // 1 character is N or S
    const longBinary = binary.slice(42, 67);  // Next 25 characters are longitude
    const longDirBinary = binary.slice(67, 68);  // 1 character is E or W
    
    const time = parseInt(timeBinary, 2)
    const hours = Math.floor(time / 3600)
    const remainingSeconds = time % 3600
    const minutes = Math.floor(remainingSeconds / 60)
    const seconds = remainingSeconds % 60

    var latitude = parseInt(latBinary, 2) / 100000
    var longitude = parseInt(longBinary, 2) / 100000
    latitude = latDirBinary === "1" ? -latitude : latitude
    longitude = longDirBinary === "1" ? -longitude : longitude

    res.json({"hours": hours, "minutes": minutes, "seconds": seconds, "latitude": latitude, "longitude": longitude })
})