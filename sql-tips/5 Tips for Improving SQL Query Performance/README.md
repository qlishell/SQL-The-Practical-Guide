# 5 Tips for Improving SQL Query Performance

Kỹ năng cơ sở dữ liệu và SQL mạnh mẽ là cần thiết cho tất cả các vai trò dữ liệu. Trong thực tế, bạn sẽ truy vấn các bảng cơ sở dữ liệu siêu lớn với hàng nghìn hoặc thậm chí hàng triệu hàng vào một ngày làm việc thông thường. Đó là lý do tại sao hiệu suất của các truy vấn SQL trở thành một yếu tố quan trọng quyết định hiệu suất tổng thể của ứng dụng.

Các truy vấn được tối ưu hóa kém thường có thể dẫn đến thời gian phản hồi chậm hơn, thời gian tải server tăng và trải nghiệm người dùng không tối ưu. Vì vậy, việc hiểu và áp dụng các kỹ thuật tối ưu hóa truy vấn SQL là điều cần thiết.

Hướng dẫn này trình bày các mẹo thực tế để tối ưu hóa các truy vấn SQL. Hãy bắt đầu.

## 1. Không sử dụng `SELECT *`; Thay vào đó hãy chọn các cột tên cụ thể

Việc người mới bắt đầu sử dụng `SELECT *` để truy xuất tất cả các cột trong bảng là điều khá phổ biến. Điều này có thể không hiệu quả nếu bạn chỉ cần một vài cột điều này hầu như luôn xảy ra. Do đó, việc sử dụng `SELECT *` có thể dẫn đến việc xử lý dữ liệu quá mức, đặc biệt nếu bảng có nhiều cột hoặc nếu bạn đang làm việc với một tập dữ liệu lớn.

```sql
-- Instead of this:
SELECT * FROM employees;

-- Do this:
SELECT employee_id, first_name, last_name FROM employees;
```

Chỉ đọc các cột cần thiết có thể làm cho các truy vấn dễ đọc và dễ bảo trì hơn.

## 2. Tránh sử dụng SELECT DISTINCT; Thay vào đó hãy sử dụng GROUP BY

`SELECT DISTINCT` có thể tốn kém vì nó yêu cầu sắp xếp và lọc kết quả để loại bỏ trùng lặp. Tốt hơn hết là đảm bảo rằng dữ liệu được truy vấn là duy nhất theo thiết kế sử dụng khóa chính hoặc các ràng buộc duy nhất.

```sql
-- Instead of this:
SELECT DISTINCT department FROM employees;

-- The following query with the GROUP BY clause is much more helpful:
SELECT department FROM employees GROUP BY department;
```

`GROUP BY` có thể hiệu quả hơn, đặc biệt là với việc lập chỉ mục phù hợp (chúng ta sẽ nói về các chỉ mục sau). Vì vậy, khi viết truy vấn, hãy đảm bảo bạn hiểu dữ liệu của mình các trường khác nhau ở cấp mô hình dữ liệu.

## 3. Giới hạn kết quả truy vấn

Thông thường, bạn sẽ truy vấn các bảng lớn có hàng nghìn hàng, nhưng không phải lúc nào bạn cũng cần (và không thể) xử lý tất cả các hàng. Việc sử dụng mệnh đề `LIMIT` (hoặc mệnh đề tương đương) giúp giảm số lượng hàng được trả về, điều này có thể tăng tốc hiệu suất truy vấn.

```sql
-- Bạn có thể giới hạn kết quả ở 15 bản ghi:
SELECT employee_id, first_name, last_name FROM employees LIMIT 15;
```

Việc sử dụng mệnh đề `LIMIT` sẽ làm giảm kích thước tập kết quả, giảm lượng dữ liệu cần xử lý và truyền. Điều này cũng hữu ích cho việc phân trang kết quả trong các ứng dụng.

## 4. Sử dụng INDEX để truy xuất nhanh hơn

Các INDEX có thể cải thiện đáng kể hiệu suất truy vấn bằng cách cho phép cơ sở dữ liệu tìm các hàng nhanh hơn việc quét toàn bộ bảng. Chúng đặc biệt hữu ích cho các cột thường được sử dụng trong các mệnh đề WHERE, JOIN và ORDER BY.

```sql
-- Đây là một INDEX mẫu được tạo trên cột 'department':
CREATE INDEX idx_employee_department ON employees(department);
```

Bây giờ bạn có thể chạy các truy vấn liên quan đến việc lọc theo cột 'department' và so sánh thời gian thực thi. Bạn sẽ thấy rằng kết quả nhanh hơn nhiều khi có `INDEX`.

Như đã đề cập, việc lập `INDEX` giúp cải thiện hiệu suất của các truy vấn lọc trên các cột đã được lập `INDEX`. Nhưng tạo quá nhiều chỉ mục có thể trở thành "thừa thãi". Điều này dẫn chúng ta đến mẹo tiếp theo!

## 5. Sử dụng INDEX một cách cẩn thận

Trong khi các `INDEX` cải thiện hiệu suất đọc, chúng có thể làm giảm hiệu suất ghi các truy vấn INSERT, UPDATE và DELETE bởi vì `INDEX` phải được cập nhật mỗi khi bảng bị thay đổi. Việc cân bằng số lượng và loại `INDEX` dựa trên loại truy vấn bạn thường chạy là rất quan trọng.

Các quy tắc cần nhớ:

-   Chỉ lập `INDEX` cho những cột thường xuyên được truy vấn.
-   Tránh lập `INDEX` thái quá trên các cột có độ đa dạng thấp (ít giá trị duy nhất).
-   Thường xuyên kiểm tra các `INDEX` và cập nhật cũng như loại bỏ chúng khi cần thiết.

## Tổng kết

Tối ưu hóa truy vấn SQL đòi hỏi bạn phải hiểu rõ yêu cầu cụ thể của truy vấn và cấu trúc dữ liệu của bạn.

Bằng cách tránh sử dụng `SELECT *`, cẩn thận khi dùng `SELECT DISTINCT`, giới hạn kết quả truy vấn `LIMIT`, tạo các `INDEX` phù hợp và luôn chú ý đến các đánh đổi khi lập `INDEX`, bạn có thể cải thiện hiệu suất và hiệu quả của các thao tác cơ sở dữ liệu một cách đáng kể.

---

HAPPY QUERYING!
