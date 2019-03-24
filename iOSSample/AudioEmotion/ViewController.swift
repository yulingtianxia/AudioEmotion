//
//  ViewController.swift
//  AudioEmotion
//
//  Created by 杨萧玉 on 2019/3/24.
//  Copyright © 2019 杨萧玉. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var recordButton: UIImageView!
    @IBOutlet weak var emotionLabel: UILabel!
    @IBOutlet weak var probabilityLabel: UILabel!
    let recorder = AudioRecorder()
    let predict = PredictAudioEmotion()
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    @IBAction func longPressButton(_ sender: UILongPressGestureRecognizer) {
        switch sender.state {
        case .began:
            if recorder?.start() ?? false {
                emotionLabel.text = "Emotion"
                probabilityLabel.text = "I'm listening..."
                recordButton.alpha = 0.5
            }
            else {
                sender.isEnabled = false
                sender.isEnabled = true
            }
        case .ended:
            if let url = recorder?.stop() {
                emotionLabel.text = "Emotion"
                probabilityLabel.text = "I'm processing..."
                DispatchQueue.global().async {
                    let results = self.predict.predictAudio(audio: url)
                    if results.count == 0 {
                        DispatchQueue.main.async {
                            self.emotionLabel.text = "Nothing"
                            self.probabilityLabel.text = "say something!"
                        }
                        return
                    }
                    let (emotion, probability) = self.predict.handlePredictionResults(results: results)
                    DispatchQueue.main.async {
                        self.emotionLabel.text = emotion
                        self.probabilityLabel.text = String(format: "%.3f", probability)
                    }
                }
            }
            recordButton.alpha = 1
        default: break
            
        }
    }
    
}

