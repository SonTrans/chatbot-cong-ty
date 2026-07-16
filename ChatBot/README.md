# Chatbot Tra Cứu Hồ Sơ Lưu Trữ - AI Assistant

## Giới thiệu

**Chatbot Tra Cứu Hồ Sơ** là một chatbot thông minh được xây dựng bằng **LangGraph** và **LangChain**, chuyên phục vụ cho nghiệp vụ tra cứu hồ sơ lưu trữ. Chatbot sử dụng kiến trúc agent kết hợp với các công cụ tra cứu mạnh mẽ thông qua Model Context Protocol (MCP), kết hợp cùng LLM để xử lý ngôn ngữ tự nhiên và trả về kết quả nhanh chóng, chính xác.

Dự án sử dụng **LangGraph** làm lõi để xây dựng và thực thi đồ thị trạng thái (state graphs), kết hợp với **LangChain** để tích hợp LLM và thiết lập kết nối đến các hệ thống khác.

## Tính năng nổi bật

- **Tích hợp Model Context Protocol (MCP)**: Trọng tâm của hệ thống, sử dụng MCP (đặc biệt là package `langchain-mcp-adapters`) để kết nối an toàn với các công cụ tra cứu và lấy dữ liệu hồ sơ từ nguồn lưu trữ ngoài một cách chuẩn hóa và linh hoạt.
  

- **Kiến trúc Agent**: Hệ thống điều phối thông qua Supervisor Agent:
- **Supervisor Agent**: Phân tích ý định người dùng và gọi các công cụ (tools) tra cứu cần thiết dựa trên yêu cầu của hồ sơ.
  
- **Cấu hình linh hoạt từ YAML**: Toàn bộ cấu hình agent, prompts, models và messages được quản lý qua các file YAML trong thư mục `Resources/`, giúp dễ dàng tùy chỉnh mà không cần can thiệp trực tiếp vào mã nguồn.

- **Quản lý trạng thái thông minh**: Quản lý `InputState` và `State` để theo dõi bối cảnh, lưu trữ thông tin các truy vấn trước đó nhằm cung cấp trải nghiệm hội thoại liên tục, mượt mà.

## Kiến trúc và cách hoạt động

Hệ thống hoạt động theo luồng sau:

1.  **Nhận yêu cầu từ người dùng**: Tin nhắn đầu vào (như thông tin cần tìm kiếm hồ sơ) được đưa vào graph thông qua schema `InputState`.

2.  **Supervisor phân tích và ra quyết định**:
    - Supervisor Node phân tích ý định của người dùng bằng cách áp dụng system prompt đã được cấu hình từ markdown.
    - Dựa vào kết quả phân tích, Agent sẽ quyết định công cụ (tool) nào cần được gọi qua MCP Server để thực hiện tra cứu.

3.  **Tương tác MCP Tools (Tra cứu dữ liệu)**:
    - Các yêu cầu được chuyển đổi thành lời gọi hàm (function calls).
    - Hệ thống gửi truy vấn đến MCP tools, công cụ sẽ tiến hành tìm kiếm hồ sơ và trả về kết quả thực tế.

4.  **Tổng hợp và trả về kết quả**:
    - State được cập nhật với kết quả trả về từ MCP tools.
    - Mô hình ngôn ngữ sẽ tổng hợp lại thành câu trả lời dễ hiểu bằng ngôn ngữ tự nhiên, sau đó gửi phản hồi cuối cùng về cho người dùng.

## Cấu trúc thư mục

```text
ChatBot/
├── Resources/                      # Tài nguyên cấu hình
│   ├── agents.yaml                 # Định nghĩa các agent trong hệ thống (PROFILE_GRAPH)
│   ├── dev.yaml                    # Cấu hình môi trường development
│   ├── messages.yaml               # Template tin nhắn
│   ├── models.yaml                 # Cấu hình các LLM models
│   ├── prompts.yaml                # Đường dẫn đến các prompt files
│   └── prompts/                    # Thư mục chứa system prompts
│       └── supervisor_prompt.md    # Prompt cho Supervisor Agent
├── src/                            # Mã nguồn chính
│   ├── common_utils/               # Các hàm tiện ích chung
│   |   ├── constants.py            # Các hằng số
│   │   ├── time_utils.py           # Xử lý thời gian
│   │   └── tools_utils.py          # Tiện ích cho tools
│   ├── config/                     # Quản lý cấu hình
│   │   └── configs.py              # Load config từ YAML
│   ├── graph/                      # Định nghĩa LangGraph
│   │   ├── agents/                 # Các agent classes
│   │   │   ├── base_agent.py       # Base class cho agents
│   │   │   └── supervisor_agent.py # Supervisor Agent
│   │   ├── nodes/                  # Các node functions
│   │   │   └── supervisor_node.py  # Node điều phối
│   │   ├── client_tools/           # MCP client tools
│   │   |   ├──  base_mcp_clinet.py # Base MCP client
│   │   ├── middlewares/            # Các middlewares xử lý trung gian
│   │   ├── configuration.py        # Cấu hình graph
│   │   ├── graph.py                # Định nghĩa graph chính
│   │   ├── state.py                # Định nghĩa State schemas
│   │   └── utils.py                # Các hàm tiện ích
│   └── log/                        # Cấu hình logging
│       |── logger.py               # Logger  
├── tests/                          # Unit & Integration tests
├── langgraph.json                  # Cấu hình LangGraph CLI
├── Makefile                        # Các lệnh tiện ích
├── pyproject.toml                  # Quản lý dependencies
└── README.md                       # Tài liệu dự án
```

## Hướng dẫn cài đặt và sử dụng

### Yêu cầu

- Python 3.10+
- Một tài khoản API từ Groq (hoặc nhà cung cấp LLM khác)
- LangGraph CLI

### Các bước cài đặt

1.  **Clone repository**:
    ```bash
    git clone <your-repository-url>
    cd ChatBot
    ```

2.  **Cài đặt dependencies**:
    ```bash
    pip install -e .
    ```

3.  **Cấu hình môi trường**:
    - Sao chép tệp `.env.example` thành `.env`:
      ```bash
      cp .env.example .env
      ```
    - Mở tệp `.env` và điền các giá trị cần thiết như cấu hình LLM (`LLM_SERVICE_HOST`, `LLM_SERVICE_API_KEY`, v.v.), các khóa API MCP và biến môi trường liên quan khác.

### Chạy ứng dụng

**Với LangGraph CLI (Development Mode)**:

```bash
langgraph dev
```

Lệnh này sẽ khởi động một server phát triển (mặc định tại `http://192.168.0.122:8090`), cung cấp giao diện [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/) để bạn tương tác trực quan, debug và thử nghiệm các truy vấn tra cứu hồ sơ thông qua chatbot.

## Tùy chỉnh

### Tùy chỉnh Graph và Nodes
Logic chính được định nghĩa trong `src/graph/graph.py`. Bạn có thể thay đổi để thêm nhiều Agent (Node) hoặc định tuyến luồng hội thoại theo yêu cầu phức tạp hơn.

### Cập nhật Prompts
Hành vi cốt lõi của Supervisor Agent nằm trong thư mục `Resources/prompts/supervisor_prompt.md`. Chỉnh sửa tập tin markdown này sẽ thay đổi cách Chatbot hiểu ý định tra cứu.

### Cấu hình Models
Chỉnh sửa `Resources/models.yaml` để tinh chỉnh tham số của mô hình:

```yaml
# Ví dụ cấu hình cho LLM
LLM_MODEL:
  MODEL_PATH: "gpt-5"
  TEMPERATURE: 0.2
  MAX_TOKENS: 4000
```

### Tích hợp MCP Tools
Khi có thêm nguồn tra cứu hồ sơ hoặc API mới:
1. Thêm kết nối tới MCP Server trong `.env` và thư mục `src/graph/client_tools/`.
2. Cấu hình schema/tool vào trong logic khởi tạo của Supervisor để Agent có thể hiểu và gọi tới công cụ đó.
