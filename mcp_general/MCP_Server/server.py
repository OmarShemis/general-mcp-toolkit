from pathlib import Path
import os

from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv(Path(__file__).resolve().parent.parent / ".env", encoding="utf-8-sig")

from tools.read_webpage import read_webpage
from tools.run_command import run_command
from tools.move_file import move_file
from tools.copy_file import copy_file
from tools.create_directory import create_directory
from tools.file_info import file_info
from tools.computer_use import create_computer_use
from tools.delete import delete
from tools.edit_file import edit_file
from tools.find_files import find_files
from tools.list_files import list_files
from tools.pdf_reader import read_pdf
from tools.read_file import read_file
from tools.search_text import search_text
from tools.web_search import web_search
from tools.write_file import write_file

mcp = FastMCP("General MCP")

for tool in (
    web_search, read_pdf, list_files, read_file, write_file,
    edit_file, delete, find_files, search_text,
    read_webpage, run_command, move_file, copy_file, create_directory, file_info,
):
    mcp.tool()(tool)

mcp.mount(create_computer_use(), namespace="computer")

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")))

