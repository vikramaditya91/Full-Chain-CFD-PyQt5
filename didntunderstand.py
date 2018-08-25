def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    self.drawLines(qp)
    qp.end()
    # currentFrame = self.movie.currentPixmap()
    # frameRect = currentFrame.rect()
    # frameRect.moveCenter(self.rect().center())
    # if frameRect.intersects(e.rect()):# and self.meshRunning == True:
    #    painter = QPainter(self)
    #    painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    self.grid = QVBoxLayout()
    # self.grid.addWidget(self.meshButton)
    self.grid.addWidget(self.on_mesh_generation_click())
    # self.grid.addStretch(1)

    self.setLayout(self.grid)

