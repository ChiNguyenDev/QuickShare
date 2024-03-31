from website import create_app

app = create_app()

# 0.0.0.0: server accessible from any network interface from host.
# server listens on port 80
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

