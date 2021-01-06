call nssm.exe install code_book_service "%cd%\run_server.bat"
call nssm.exe set code_book_service AppStdout "%cd%\logs\code_book_service.log"
call nssm.exe set code_book_service AppStderr "%cd%\logs\code_book_service.log"
call sc start code_book_service
rem call nssm.exe edit code_book_service