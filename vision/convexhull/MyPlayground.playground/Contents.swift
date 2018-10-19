import Foundation

class Point {
    let x: Int
    let y: Int
    
    init(_ x: Int, _ y: Int) {
        self.x = x
        self.y = y
    }
    
}


func slope(_ p1: Point, _ p2: Point) -> Double {
    return Double(p2.y - p1.y)/Double(p2.x-p1.x);
}

let testImageArr: [Int] = [5, 2, 2, 2, 1, 1, 3, 3, 3, 2, 2, 1, 1, 1, 0, 0]

func generateImageFromArray(arr: [Int], ySize: Int) -> [[Bool]]{
    
    var image: [[Bool]] = Array(repeating: Array(repeating: false, count: 5), count: arr.count)
    
    for x in 0..<arr.count {
        var y = 0;

        while y < arr[x] {
            image[x][y] = true
            y = y + 1
        }
        
        while y < ySize {
            image[x][y] = false
            y = y + 1
        }
    }
    
    return image
}


let testImage = generateImageFromArray(arr: testImageArr, ySize: 5)


func convexHull(image: [[Bool]]) -> [Point] {

    var list: [Point] = []
    list.append(Point(0, image[0].count-1))
    
    var prev = 0;
    for x in 0..<image.count {
        var curr: Point? = nil
        
        for y in (0...(image[x].count-1)).reversed() {
            //print("==\(x),\(y)")
            if image[x][y] {
                curr = Point(x, y)
                print("(\(curr!.x), \(curr!.y))")
                break;
            }
        }
        
        guard let currPoint = curr else {
            continue;
        }
        
        var prevSlope: Double
        repeat {
            prevSlope = (prev == 0) ? Double.infinity : slope(list[prev-1], list[prev])
            if prevSlope < slope(list[prev], currPoint) {
                list.remove(at: prev)
                prev = prev - 1
            } else {
                list.append(currPoint)
                prev = prev + 1
                break;
            }
        } while true
      
    }
    
    return list
}


print(testImage)
for point in convexHull(image: testImage) {
    print("\(point.x) \(point.y)")
}
