package crawl;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class App {
    public static void main(String[] args) throws InterruptedException, IOException {

        System.out.println("Nhập từ khóa muốn tìm kiếm: ");
        Scanner scan = new Scanner(System.in);
        String key = scan.nextLine();

        System.setProperty("webdriver.edge.driver",
                "C:/Users/Admin/OneDrive/Documents/edgedriver_win64/msedgedriver.exe");
        System.setProperty("webdriver.chrome.driver", "E:/JAVA (tester)/chromedriver_win32/chromedriver.exe");
        WebDriver driver = new ChromeDriver();

        driver.get("https://www.google.com.vn/?hl=vi");
        driver.findElement(By.xpath("//*[@title='Tìm kiếm']")).sendKeys(key);
        Thread.sleep(1000);
        driver.findElement(By.xpath("//li[@role='presentation'][1]")).click();
        driver.findElement(By.xpath("//a[text()='Hình ảnh']")).click();
        JavascriptExecutor js = (JavascriptExecutor) driver;
        js.executeScript("window.scrollBy(0,600)");
        Thread.sleep(10000);
        List<WebElement> images = driver.findElements(By.xpath("//img"));
        List<String> srcImg = new ArrayList();
        for (WebElement i : images) {
            srcImg.add(i.getAttribute("src"));
        }
        int k = 0;

        for (String i : srcImg) {
            try {

                URL url = new URL(i);
                InputStream is = url.openStream();
                // OutputStream os = new FileOutputStream("E:\\JAVA
                // (tester)\\crawl\\result\\img" + k + ".png");
                // byte[] b = new byte[2048];
                // int length;
                // while ((length = is.read(b)) != -1) {
                // os.write(b, 0, length);
                // }
                Files.copy(is, Paths.get("E:\\JAVA (tester)\\crawl\\result\\img" + k +
                        ".jpg"));

                k++;
            } catch (IOException e) {
                System.out.println("Fail");
            }

        }

    }
}
