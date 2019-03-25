//
//  RecordButton.swift
//  AudioEmotion
//
//  Created by 杨萧玉 on 2019/3/25.
//  Copyright © 2019 杨萧玉. All rights reserved.
//

import UIKit

protocol RecordProtocol : class {
    func beginRecord()
    func finishedRecord(url: URL)
}

class RecordButton: UIImageView {
    
    let recorder = AudioRecorder()
    var recording = false
    weak var delegate: RecordProtocol?
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        if recording {
            return
        }
        if recorder?.start() ?? false {
            alpha = 0.5
            recording = true
            delegate?.beginRecord()
        }
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        if recording {
            if let url = recorder?.stop() {
                delegate?.finishedRecord(url: url)
                recording = false
            }
            alpha = 1
        }
    }
}
