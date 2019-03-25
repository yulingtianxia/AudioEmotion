//
//  ViewController.swift
//  AudioEmotion
//
//  Created by 杨萧玉 on 2019/3/24.
//  Copyright © 2019 杨萧玉. All rights reserved.
//

import UIKit
import AVFoundation

class ViewController: UIViewController, RecordProtocol {
    
    @IBOutlet weak var recordButton: RecordButton!
    @IBOutlet weak var emotionLabel: UILabel!
    @IBOutlet weak var probabilityLabel: UILabel!
    
    let predict = PredictAudioEmotion()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        if AVCaptureDevice.authorizationStatus(for: .audio) == .authorized {
            self.recordButton.isUserInteractionEnabled = true
        }
        else {
            AVCaptureDevice.requestAccess(for: .audio) { (result) in
                DispatchQueue.main.async {
                    self.recordButton.isUserInteractionEnabled = result
                }
            }
        }
        recordButton.delegate = self
    }

    func beginRecord() {
        emotionLabel.text = "Emotion"
        probabilityLabel.text = "I'm listening..."
    }
    
    func finishedRecord(url: URL) {
        emotionLabel.text = "Emotion"
        probabilityLabel.text = "I'm processing..."
        DispatchQueue.global().async {
            guard let results = self.predict.predictAudio(audio: url) else {
                self.showEmptyResult()
                return
            }
            if results.count == 0 {
                self.showEmptyResult()
                return
            }
            let (emotion, probability) = self.predict.handlePredictionResults(results: results)
            DispatchQueue.main.async {
                self.emotionLabel.text = emotion
                self.probabilityLabel.text = String(format: "%.3f", probability)
            }
        }
    }
    
    func showEmptyResult() {
        DispatchQueue.main.async {
            self.emotionLabel.text = "Nothing"
            self.probabilityLabel.text = "say something!"
        }
    }
    
}

